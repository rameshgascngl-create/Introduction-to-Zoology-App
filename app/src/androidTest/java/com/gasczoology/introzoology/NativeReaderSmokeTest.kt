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
        val dir = File(context.getExternalFilesDir(null), "qa-screenshots")
        dir.mkdirs()
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

    @Test fun quizAnswerSurvivesRotation() {
        englishHome()
        rule.onNodeWithTag("navQuiz").performClick()
        rule.onNodeWithTag("quiz-answer-0-0").performClick()
        rule.onNodeWithTag("quiz-answer-0-0").assertIsSelected()
        shot("05-quiz-portrait")
        rule.activityRule.scenario.onActivity {
            it.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        }
        rule.waitForIdle()
        rule.onNodeWithTag("quiz-answer-0-0").assertIsSelected()
        shot("06-quiz-landscape")
    }
}
