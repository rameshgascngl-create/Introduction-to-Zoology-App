package com.gasczoology.introzoology

import android.content.pm.ActivityInfo
import android.graphics.Bitmap
import android.content.ContentValues
import android.provider.MediaStore
import android.os.Environment
import android.os.SystemClock
import android.util.Log
import androidx.compose.ui.graphics.asAndroidBitmap
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.By
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class NativeReaderSmokeTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()

    /** Capture actual on-device pixels; use Compose only if UiAutomation has no frame.
     * The fallback still captures the rendered Android Compose UI. A missing
     * image or missing semantics remains a hard test failure.
     */
    private fun captureEvidenceBitmap(label: String): Bitmap {
        val automation = InstrumentationRegistry.getInstrumentation().uiAutomation
        repeat(4) { attempt ->
            rule.waitForIdle()
            val frame = runCatching { automation.takeScreenshot() }
                .onFailure { Log.w("IntroZoologyQA", "Screenshot attempt ${attempt + 1} failed: $label", it) }
                .getOrNull()
            if (frame != null && frame.width >= 320 && frame.height >= 320) return frame
            frame?.recycle()
            SystemClock.sleep(400L)
        }
        Log.w("IntroZoologyQA", "UiAutomation unavailable for $label; capturing Compose root")
        return try {
            rule.onRoot().captureToImage().asAndroidBitmap().also { frame ->
                check(frame.width >= 320 && frame.height >= 320) {
                    "Compose fallback is too small: $label"
                }
            }
        } catch (cause: Throwable) {
            throw IllegalStateException("Both screenshot methods failed: $label", cause)
        }
    }

    private fun shot(label: String) {
        rule.waitForIdle()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        // Save to the shared MediaStore collection, not app-private storage.
        // Gradle's connectedAndroidTest may remove the debug APK before
        // screenshot collection, making "adb run-as" fail after test success.
        val bmp = captureEvidenceBitmap(label)
        val resolver = context.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, "$label.png")
            put(MediaStore.Images.Media.MIME_TYPE, "image/png")
            put(
                MediaStore.Images.Media.RELATIVE_PATH,
                "${Environment.DIRECTORY_PICTURES}/IntroductionZoologyQA/"
            )
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
        val uri = checkNotNull(
            resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
        ) { "MediaStore insert failed: $label" }
        try {
            checkNotNull(resolver.openOutputStream(uri)) {
                "MediaStore output stream failed: $label"
            }.use { out ->
                check(bmp.compress(Bitmap.CompressFormat.PNG, 100, out)) {
                    "PNG encode failed: $label"
                }
            }
            resolver.update(uri, ContentValues().apply {
                put(MediaStore.Images.Media.IS_PENDING, 0)
            }, null, null)
        } catch (error: Exception) {
            resolver.delete(uri, null, null)
            throw error
        } finally {
            bmp.recycle()
        }
        // Compose semantics can pass while Android System UI is stuck over
        // the app. Visual QA MUST NOT accept screenshots behind an ANR dialog.
        val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
        val blocked = listOf("isn't responding", "is not responding",
            "keeps stopping", "has stopped").any { phrase ->
            device.hasObject(By.textContains(phrase))
        }
        check(!blocked) {
            "VISUAL_QA_BLOCKED: Android system or app error dialog obscures $label"
        }
    }

    private fun englishHome() {
        rule.onNodeWithTag("navHome").performClick()
        rule.waitForIdle()
        val titleVisible = rule.onAllNodesWithText("Introduction to Zoology").fetchSemanticsNodes().isNotEmpty()
        if (!titleVisible) rule.onNodeWithTag("languageToggle").performClick()
        rule.waitForIdle()
    }

    @Test fun chaptersDiagramsAndTamil() {
        englishHome()
        shot("01-home-en")
        rule.onNodeWithTag("unit-1").performClick()
        rule.onNodeWithTag("chapter-1.1").performClick()
        rule.onNodeWithTag("chapterScroller")
            .performScrollToNode(hasTestTag("plate-systflow"))
        rule.onNodeWithTag("plate-systflow").performClick()
        rule.onNodeWithTag("plateDialog").assertExists()
        shot("02-diagram-fullscreen")
        rule.onNodeWithContentDescription("Close image").performClick()
        rule.onNodeWithTag("languageToggle").performClick()
        rule.onNodeWithText("விலங்கியல் அறிமுகம்").assertExists()
        shot("03-chapter-tamil")
    }

    @Test fun bookmarksPersistAfterRecreation() {
        englishHome()
        rule.onNodeWithTag("unit-1").performClick()
        rule.onNodeWithTag("chapter-1.1").performClick()
        rule.onNodeWithTag("bookmarkToggle").performClick()
        rule.activityRule.scenario.recreate()
        rule.waitForIdle()
        rule.onNodeWithTag("bookmarkToggle").assertExists()
        rule.onNodeWithContentDescription("Back").performClick()
        rule.onNodeWithTag("navSaved").performClick()
        rule.onNodeWithTag("chapter-1.1").assertExists()
        shot("04-bookmark-saved")
    }

    @Test fun fiveSyllabusUnitsNavigateAndTamilIsAccessible() {
        englishHome()
        for (unit in 1..5) {
            rule.onNodeWithTag("homeScroller").performScrollToNode(hasTestTag("unit-$unit"))
            rule.onNodeWithTag("unit-$unit").performClick()
            rule.onNodeWithTag("chapter-$unit.1").assertExists()
            rule.onNodeWithTag("navHome").performClick()
        }
        rule.onNodeWithTag("languageToggle").performClick()
        rule.onNodeWithText("விலங்கியல் அறிமுகம்").assertExists()
        shot("07-all-units-tamil")
    }

    @Test fun quizAnswerSurvivesRotation() {
        englishHome()
        rule.onNodeWithTag("navQuiz").performClick()
        rule.onNodeWithTag("quizScroller").performScrollToNode(hasTestTag("quiz-answer-0-0"))
        rule.onNodeWithTag("quiz-answer-0-0").performClick()
        rule.onNodeWithTag("quiz-answer-0-0").assertIsSelected()
        shot("05-quiz-portrait")
        rule.activityRule.scenario.onActivity {
            it.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        }
        rule.waitForIdle()
        shot("06-quiz-landscape-before-scroll")
        rule.onNodeWithTag("quizScroller").performScrollToNode(hasTestTag("quiz-answer-0-0"))
        rule.onNodeWithTag("quiz-answer-0-0").assertIsSelected()
        shot("06-quiz-landscape")
        // The answer must also survive leaving and re-entering the quiz.
        rule.onNodeWithTag("navHome").performClick()
        rule.onNodeWithTag("navQuiz").performClick()
        rule.onNodeWithTag("quizScroller").performScrollToNode(hasTestTag("quiz-answer-0-0"))
        rule.onNodeWithTag("quiz-answer-0-0").assertIsSelected()
    }

    @Test fun chapterFiveHoneyBeePlateRendersInEnglishAndTamil() {
        englishHome()
        rule.onNodeWithTag("homeScroller").performScrollToNode(hasTestTag("unit-5"))
        rule.onNodeWithTag("unit-5").performClick()
        rule.onNodeWithTag("chapter-5.2").performClick()
        rule.onNodeWithTag("chapterScroller").performScrollToNode(hasTestTag("plate-bee"))
        rule.onNodeWithTag("plate-bee").performClick()
        rule.onNodeWithTag("plateDialog").assertExists()
        check(rule.onAllNodesWithContentDescription("Honey-bee Colony Organisation")
            .fetchSemanticsNodes().isNotEmpty()) { "Honey-bee PNG is not rendered in English" }
        shot("08-bee-plate-en")
        rule.onNodeWithContentDescription("Close image").performClick()
        rule.onNodeWithTag("languageToggle").performClick()
        rule.onNodeWithTag("chapterScroller").performScrollToNode(hasTestTag("plate-bee"))
        rule.onNodeWithTag("plate-bee").performClick()
        rule.onNodeWithTag("plateDialog").assertExists()
        check(rule.onAllNodesWithContentDescription("தேனீக் கூட்டத்தின் அமைப்பு")
            .fetchSemanticsNodes().isNotEmpty()) { "Honey-bee PNG is not rendered in Tamil" }
        shot("09-bee-plate-ta")
    }
}
