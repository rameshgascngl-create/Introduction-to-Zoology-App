package com.gasczoology.introzoology

import android.content.pm.ActivityInfo
import android.graphics.Bitmap
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.io.FileOutputStream
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class NativeReaderSmokeTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()

    private fun shot(label: String) {
        rule.waitForIdle()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        // External storage can be unavailable while an emulator is booting.
        // Always write to the app's internal files directory, then collect
        // the screenshots with "adb exec-out run-as" from the debug build.
        val dir = File(context.filesDir, "qa-screenshots")
        check(dir.isDirectory || dir.mkdirs()) {
            "Cannot create screenshot folder: ${dir.absolutePath}"
        }
        val bmp = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
        if (bmp != null) {
            FileOutputStream(File(dir, "$label.png")).use { out ->
                bmp.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            bmp.recycle()
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
}
