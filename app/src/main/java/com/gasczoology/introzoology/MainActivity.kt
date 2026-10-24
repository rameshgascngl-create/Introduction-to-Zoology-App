package com.gasczoology.introzoology

import android.content.Context
import android.graphics.BitmapFactory
import android.os.Bundle
import android.text.Html
import android.text.method.LinkMovementMethod
import android.util.TypedValue
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.mapSaver
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import org.json.JSONObject
import kotlin.math.roundToInt

/* Native Jetpack Compose and Android TextView ONLY; no WebView, WebViewAssetLoader,
 * HTML document runtime, JavaScript engine, or Internet permission. */

private val Green = Color(0xFF146B52)
private val Navy = Color(0xFF17324D)
private val Canvas = Color(0xFFF4F7F9)

private data class UnitEntry(
    val id: Int, val enTitle: String, val taTitle: String,
    val enSubtitle: String, val taSubtitle: String,
    val enBridge: String, val taBridge: String
)
private data class ChapterEntry(
    val id: String, val unit: Int, val number: Int,
    val enTitle: String, val taTitle: String,
    val contentEn: String, val contentTa: String,
    val misEn: String, val misTa: String,
    val activityEn: String, val activityTa: String
)
private data class TeachingPlate(
    val id: String, val chapter: String,
    val enTitle: String, val taTitle: String,
    val enCap: String, val taCap: String,
    val filename: String, val kind: String
)
private data class QuizQuestion(val question: String, val options: List<String>, val answer: Int, val rationale: String)
private data class QuestionBank(
    val mcqEn: List<QuizQuestion>, val mcqTa: List<QuizQuestion>,
    val shortEn: List<String>, val shortTa: List<String>,
    val longEn: List<String>, val longTa: List<String>
)
private data class Syllabus(
    val units: List<UnitEntry>, val chapters: List<ChapterEntry>,
    val plates: List<TeachingPlate>, val questionBank: Map<Int, QuestionBank>
) {
    companion object {
        fun load(context: Context): Syllabus {
            val obj = JSONObject(context.assets.open("content.json").bufferedReader(Charsets.UTF_8).use { it.readText() })
            val units = obj.getJSONArray("units")
            val chapters = obj.getJSONArray("chapters")
            val plates = obj.getJSONArray("plates")
            val exams = obj.getJSONObject("questionBank")
            fun readStrings(j: org.json.JSONArray) = (0 until j.length()).map { j.getString(it) }
            fun questions(j: org.json.JSONArray) = (0 until j.length()).map { i ->
                val q = j.getJSONObject(i)
                QuizQuestion(q.getString("q"), readStrings(q.getJSONArray("o")),
                    q.getString("a").first().uppercaseChar() - 'A', q.optString("r", ""))
            }
            val questionBank = (1..5).associateWith { id ->
                val b = exams.getJSONObject(id.toString())
                QuestionBank(questions(b.getJSONArray("mcqEn")), questions(b.getJSONArray("mcqTa")),
                    readStrings(b.getJSONArray("bEn")), readStrings(b.getJSONArray("bTa")),
                    readStrings(b.getJSONArray("cEn")), readStrings(b.getJSONArray("cTa")))
            }
            return Syllabus(
                (0 until units.length()).map { i -> units.getJSONObject(i).run {
                    UnitEntry(getInt("id"), getString("enTitle"), getString("taTitle"),
                        getString("enSubtitle"), getString("taSubtitle"),
                        getString("enBridge"), getString("taBridge"))
                } },
                (0 until chapters.length()).map { i -> chapters.getJSONObject(i).run {
                    ChapterEntry(getString("id"), getInt("unit"), getInt("n"),
                        getString("enTitle"), getString("taTitle"),
                        getString("contentEn"), getString("contentTa"),
                        getString("misEn"), getString("misTa"),
                        getString("activityEn"), getString("activityTa"))
                } },
                (0 until plates.length()).map { i -> plates.getJSONObject(i).run {
                    TeachingPlate(getString("id"), getString("chapter"),
                        getString("enTitle"), getString("taTitle"),
                        getString("enCap"), getString("taCap"),
                        getString("filename"), getString("kind"))
                } }, questionBank
            )
        }
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val syllabus = Syllabus.load(this)
        setContent {
            val dark = androidx.compose.foundation.isSystemInDarkTheme()
            MaterialTheme(
                colorScheme = if (dark) darkColorScheme(primary = Color(0xFF83D6B9))
                else lightColorScheme(primary = Green, secondary = Navy, background = Canvas,
                    surface = Color.White, surfaceVariant = Color(0xFFE5F0ED)),
            ) { ZoologyApp(syllabus) }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ZoologyApp(data: Syllabus) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("native_intro_zoology_v6", Context.MODE_PRIVATE) }
    var tamil by rememberSaveable { mutableStateOf(prefs.getBoolean("tamil", false)) }
    var textSize by rememberSaveable { mutableFloatStateOf(prefs.getFloat("text_size", 17f)) }
    var view by rememberSaveable { mutableStateOf("home") }
    var returnView by rememberSaveable { mutableStateOf("unit") }
    var currentUnit by rememberSaveable { mutableIntStateOf(1) }
    var currentChapter by rememberSaveable { mutableStateOf(data.chapters.first().id) }
    var query by rememberSaveable { mutableStateOf("") }
    val completed = remember { mutableStateListOf<String>().apply { addAll(prefs.getStringSet("completed", emptySet()).orEmpty()) } }
    val bookmarks = remember { mutableStateListOf<String>().apply { addAll(prefs.getStringSet("bookmarks", emptySet()).orEmpty()) } }
    val lastRead = remember { mutableStateOf(prefs.getString("last_chapter", "") ?: "") }
    var testUnit by rememberSaveable { mutableIntStateOf(1) }
    val chosen = data.chapters.firstOrNull { it.id == currentChapter } ?: data.chapters.first()
    val unit = data.units.firstOrNull { it.id == currentUnit } ?: data.units.first()
    val chapterList = data.chapters.filter { it.unit == currentUnit }
    val currentIndex = chapterList.indexOfFirst { it.id == chosen.id }.coerceAtLeast(0)

    fun openChapter(chapter: ChapterEntry) {
        returnView = if (view == "chapter") "unit" else view
        currentUnit = chapter.unit
        currentChapter = chapter.id
        lastRead.value = chapter.id
        prefs.edit().putString("last_chapter", chapter.id).apply()
        view = "chapter"
    }
    fun back() {
        view = when (view) {
            "chapter" -> returnView
            "unit", "search", "bookmarks", "quiz" -> "home"
            else -> "home"
        }
    }
    BackHandler(enabled = view != "home") { back() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(if (tamil) "விலங்கியல் அறிமுகம்" else "Introduction to Zoology",
                            fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(if (view == "chapter") "${chosen.id}  ·  ${if (tamil) "பாடம்" else "Chapter"}"
                             else if (view == "unit") "${if (tamil) "அலகு" else "Unit"} $currentUnit"
                             else "Native textbook · ${BuildConfig.VERSION_NAME}", fontSize = 12.sp)
                    }
                },
                navigationIcon = {
                    if (view != "home") IconButton(onClick = { back() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = if (tamil) "பின்செல்க" else "Back")
                    } else Icon(Icons.Default.MenuBook, contentDescription = null,
                        modifier = Modifier.padding(horizontal = 14.dp), tint = MaterialTheme.colorScheme.primary)
                },
                actions = {
                    TextButton(modifier = Modifier.testTag("languageToggle"), onClick = {
                        tamil = !tamil
                        prefs.edit().putBoolean("tamil", tamil).apply()
                    }) { Text(if (tamil) "EN" else "தமிழ்", fontWeight = FontWeight.Bold) }
                    if (view == "chapter") {
                        IconButton(modifier = Modifier.testTag("bookmarkToggle"), onClick = {
                            if (chosen.id in bookmarks) bookmarks.remove(chosen.id) else bookmarks.add(chosen.id)
                            prefs.edit().putStringSet("bookmarks", bookmarks.toSet()).apply()
                        }) {
                            Icon(if (chosen.id in bookmarks) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                                contentDescription = if (tamil) "புத்தகக்குறி" else "Bookmark")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        },
        bottomBar = {
            if (view != "chapter") NavigationBar(containerColor = MaterialTheme.colorScheme.surface) {
                NavigationBarItem(selected = view == "home" || view == "unit", onClick = { view = "home" },
                    modifier = Modifier.testTag("navHome"),
                    icon = { Icon(Icons.Default.Home, contentDescription = null) },
                    label = { Text(if (tamil) "முகப்பு" else "Home") })
                NavigationBarItem(selected = view == "search", onClick = { view = "search" },
                    modifier = Modifier.testTag("navSearch"),
                    icon = { Icon(Icons.Default.Search, contentDescription = null) },
                    label = { Text(if (tamil) "தேடல்" else "Search") })
                NavigationBarItem(selected = view == "bookmarks", onClick = { view = "bookmarks" },
                    modifier = Modifier.testTag("navSaved"),
                    icon = { Icon(Icons.Default.Bookmarks, contentDescription = null) },
                    label = { Text(if (tamil) "சேமித்தவை" else "Saved") })
                NavigationBarItem(selected = view == "quiz", onClick = { view = "quiz" },
                    modifier = Modifier.testTag("navQuiz"),
                    icon = { Icon(Icons.Default.Quiz, contentDescription = null) },
                    label = { Text(if (tamil) "வினாக்கள்" else "Tests") })
            }
        }
    ) { inner ->
        when (view) {
            "home" -> HomeScreen(data, tamil, completed, lastRead.value,
                onUnit = { currentUnit = it; view = "unit" }, onContinue = { id ->
                    data.chapters.find { it.id == id }?.let { openChapter(it) }
                }, modifier = Modifier.padding(inner))
            "unit" -> UnitScreen(unit, chapterList, tamil, completed, bookmarks,
                onChapter = { openChapter(it) }, modifier = Modifier.padding(inner))
            "search" -> SearchScreen(data, query, { query = it }, tamil, completed,
                onChapter = { openChapter(it) }, modifier = Modifier.padding(inner))
            "bookmarks" -> SavedScreen(data.chapters.filter { it.id in bookmarks }, tamil, completed,
                onChapter = { openChapter(it) }, modifier = Modifier.padding(inner))
            "quiz" -> QuestionScreen(data.questionBank, tamil, testUnit, onUnit = { testUnit = it },
                modifier = Modifier.padding(inner))
            // A chapter is a new reading page: Compose must not retain the previous
            // LazyColumn's scroll index or offset when Next/Previous changes its ID.
            "chapter" -> key(chosen.id) {
                ChapterScreen(chosen, chapterList, currentIndex,
                    data.plates.filter { it.chapter == chosen.id }, tamil, textSize,
                    completed.contains(chosen.id),
                    onTextSize = { textSize = it; prefs.edit().putFloat("text_size", textSize).apply() },
                    onCompleted = { done ->
                        if (done && chosen.id !in completed) completed.add(chosen.id)
                        if (!done) completed.remove(chosen.id)
                        prefs.edit().putStringSet("completed", completed.toSet()).apply()
                    },
                    onChapter = { openChapter(it) }, modifier = Modifier.padding(inner))
            }
        }
    }
}

@Composable
private fun HomeScreen(data: Syllabus, tamil: Boolean, completed: List<String>,
    lastRead: String, onUnit: (Int) -> Unit, onContinue: (String) -> Unit, modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier.testTag("homeScroller").fillMaxSize().background(MaterialTheme.colorScheme.background),
        contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item {
            Column(Modifier.fillMaxWidth().background(Navy, RoundedCornerShape(18.dp)).padding(22.dp)) {
                Text(if (tamil) "ஐந்து அலகுகள் · ${data.chapters.size} பாடங்கள்" else "5 units · ${data.chapters.size} chapters",
                    color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(6.dp))
                Text(if (tamil) "விரிவான இருமொழி விலங்கியல் பாடநூல் — இணையம் தேவையில்லை"
                     else "Bilingual undergraduate Zoology, redesigned for offline native Android reading.",
                    color = Color(0xFFE5F1EB), fontSize = 14.sp)
                Spacer(Modifier.height(15.dp))
                LinearProgressIndicator(progress = { completed.size.toFloat() / data.chapters.size.coerceAtLeast(1) }, modifier = Modifier.fillMaxWidth(),
                    color = Color(0xFF8EE0B7), trackColor = Color(0xFF587388))
                Spacer(Modifier.height(6.dp))
                Text("${completed.size}/${data.chapters.size} ${if (tamil) "பாடங்கள் முடிக்கப்பட்டன" else "chapters completed"}",
                    color = Color.White, fontSize = 12.sp)
                if (lastRead.isNotBlank()) {
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = { onContinue(lastRead) }, colors = ButtonDefaults.buttonColors(
                        containerColor = Color.White, contentColor = Navy)) {
                        Icon(Icons.Default.PlayArrow, contentDescription = null)
                        Spacer(Modifier.width(5.dp))
                        Text(if (tamil) "மீண்டும் படிக்க" else "Continue chapter $lastRead")
                    }
                }
            }
        }
        item { Text(if (tamil) "பாட அலகுகள்" else "Explore the syllabus", fontSize = 19.sp, fontWeight = FontWeight.Bold) }
        items(data.units, key = { it.id }) { u ->
            val count = data.chapters.count { it.unit == u.id }
            val done = data.chapters.count { it.unit == u.id && it.id in completed }
            Card(onClick = { onUnit(u.id) }, modifier = Modifier.testTag("unit-${u.id}"), shape = RoundedCornerShape(14.dp)) {
                Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(12.dp)) {
                            Text("${u.id}", modifier = Modifier.padding(horizontal = 13.dp, vertical = 8.dp),
                                fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        }
                        Spacer(Modifier.width(12.dp))
                        Column(Modifier.weight(1f)) {
                            Text(if (tamil) u.taTitle else u.enTitle, fontWeight = FontWeight.SemiBold, fontSize = 17.sp)
                            Text(if (tamil) u.taSubtitle else u.enSubtitle,
                                color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, maxLines = 2)
                        }
                        Icon(Icons.Default.ChevronRight, contentDescription = null)
                    }
                    LinearProgressIndicator(progress = { if (count == 0) 0f else done.toFloat() / count },
                        modifier = Modifier.fillMaxWidth())
                    Text("$done / $count ${if (tamil) "பாடங்கள்" else "chapters"}", fontSize = 12.sp)
                }
            }
        }
        item {
            Text(if (tamil) "விலங்கியல் துறை · அரசு கலை மற்றும் அறிவியல் கல்லூரி, நாகர்கோவில்"
                else "Department of Zoology · Government Arts and Science College, Nagercoil",
                color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
        }
    }
}

@Composable
private fun UnitScreen(unit: UnitEntry, chapters: List<ChapterEntry>, tamil: Boolean,
    completed: List<String>, bookmarks: List<String>, onChapter: (ChapterEntry) -> Unit,
    modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background),
        contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            Text(if (tamil) "அலகு ${unit.id}" else "UNIT ${unit.id}", color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold)
            Text(if (tamil) unit.taTitle else unit.enTitle, fontSize = 23.sp, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(7.dp))
            Text(if (tamil) unit.taBridge else unit.enBridge, fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        items(chapters, key = { it.id }) { chapter ->
            ChapterTile(chapter, tamil, chapter.id in completed, chapter.id in bookmarks, onClick = { onChapter(chapter) })
        }
    }
}

@Composable
private fun ChapterTile(chapter: ChapterEntry, tamil: Boolean, done: Boolean, saved: Boolean,
    onClick: () -> Unit) {
    Card(onClick = onClick, modifier = Modifier.testTag("chapter-${chapter.id}"), shape = RoundedCornerShape(12.dp)) {
        Row(Modifier.fillMaxWidth().padding(15.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text("${if (tamil) "பாடம்" else "CHAPTER"} ${chapter.id}",
                    fontSize = 11.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.height(3.dp))
                Text(if (tamil) chapter.taTitle else chapter.enTitle, fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
            }
            if (saved) Icon(Icons.Default.Bookmark, contentDescription = "Saved", tint = MaterialTheme.colorScheme.primary)
            if (done) {
                Spacer(Modifier.width(5.dp))
                Icon(Icons.Default.CheckCircle, contentDescription = "Completed", tint = Green)
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null)
        }
    }
}

@Composable
private fun SearchScreen(data: Syllabus, query: String, onQuery: (String) -> Unit,
    tamil: Boolean, completed: List<String>, onChapter: (ChapterEntry) -> Unit, modifier: Modifier = Modifier) {
    val found = remember(query, tamil) {
        if (query.isBlank()) data.chapters else data.chapters.filter { c ->
            c.id.contains(query, ignoreCase = true) || c.enTitle.contains(query, ignoreCase = true) ||
                c.taTitle.contains(query, ignoreCase = true) ||
                c.contentEn.contains(query, ignoreCase = true) || c.contentTa.contains(query, ignoreCase = true)
        }
    }
    Column(modifier.fillMaxSize().padding(15.dp)) {
        OutlinedTextField(value = query, onValueChange = onQuery, singleLine = true,
            label = { Text(if (tamil) "பாடங்களில் தேடுக" else "Search all chapters and concepts") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            modifier = Modifier.fillMaxWidth())
        Text("${found.size} ${if (tamil) "பாடங்கள்" else "chapters found"}",
            modifier = Modifier.padding(vertical = 10.dp), fontSize = 12.sp)
        LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            items(found, key = { it.id }) { ch ->
                ChapterTile(ch, tamil, ch.id in completed, false, onClick = { onChapter(ch) })
            }
        }
    }
}

@Composable
private fun SavedScreen(chapters: List<ChapterEntry>, tamil: Boolean, completed: List<String>,
    onChapter: (ChapterEntry) -> Unit, modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier.fillMaxSize(), contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item {
            Text(if (tamil) "சேமித்த பாடங்கள்" else "Bookmarked chapters", fontSize = 22.sp, fontWeight = FontWeight.Bold)
        }
        if (chapters.isEmpty()) item {
            Text(if (tamil) "சேமிக்கப்பட்ட பாடங்கள் இல்லை. பாடத்தில் உள்ள குறியைத் தட்டவும்."
                else "No bookmarks yet. Save chapters using the bookmark icon in the reader.")
        }
        items(chapters, key = { it.id }) { ch ->
            ChapterTile(ch, tamil, ch.id in completed, true, onClick = { onChapter(ch) })
        }
    }
}

@Composable
private fun ChapterScreen(chapter: ChapterEntry, chapterList: List<ChapterEntry>, index: Int,
    diagrams: List<TeachingPlate>, tamil: Boolean, textSize: Float, completed: Boolean,
    onTextSize: (Float) -> Unit, onCompleted: (Boolean) -> Unit,
    onChapter: (ChapterEntry) -> Unit, modifier: Modifier = Modifier) {
    var expanded by remember(chapter.id) { mutableStateOf<TeachingPlate?>(null) }
    LazyColumn(modifier = modifier.testTag("chapterScroller").fillMaxSize().background(MaterialTheme.colorScheme.background),
        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 12.dp, bottom = 26.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item(key = "heading") {
            Text("${if (tamil) "அலகு" else "UNIT"} ${chapter.unit} · ${if (tamil) "பாடம்" else "CHAPTER"} ${chapter.id}",
                color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(4.dp))
            Text(if (tamil) chapter.taTitle else chapter.enTitle, fontSize = 24.sp,
                fontWeight = FontWeight.Bold, lineHeight = 30.sp)
            Spacer(Modifier.height(12.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(if (tamil) "எழுத்து அளவு" else "Text size", fontSize = 12.sp,
                    modifier = Modifier.weight(1f))
                OutlinedButton(onClick = { onTextSize((textSize - 1f).coerceAtLeast(14f)) },
                    contentPadding = PaddingValues(horizontal = 14.dp, vertical = 4.dp)) { Text("A−") }
                Spacer(Modifier.width(7.dp))
                OutlinedButton(onClick = { onTextSize((textSize + 1f).coerceAtMost(24f)) },
                    contentPadding = PaddingValues(horizontal = 14.dp, vertical = 4.dp)) { Text("A+") }
            }
        }
        item(key = "lesson") {
            Card(shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(16.dp)) {
                    Text(if (tamil) "விரிவான பாட விளக்கம்" else "CONCEPTS & EXPLANATIONS",
                        color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    Spacer(Modifier.height(12.dp))
                    NativeRichText(html = if (tamil) chapter.contentTa else chapter.contentEn, size = textSize)
                }
            }
        }
        item(key = "diagram_title") {
            Text("${if (tamil) "பெயரிடப்பட்ட விளக்கப்படங்கள்" else "Labelled diagrams"}  ·  ${diagrams.size}",
                fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Text(if (tamil) "பெரிதாக்கத் தட்டவும்; முழுத்திரையில் விரல்களால் அளவை மாற்றலாம்."
                 else "Tap a plate to view full-screen. Pinch to zoom.", fontSize = 12.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        items(diagrams, key = { "plate-${it.id}" }) { plate ->
            Card(onClick = { expanded = plate }, modifier = Modifier.testTag("plate-${plate.id}"), shape = RoundedCornerShape(14.dp)) {
                Column(Modifier.fillMaxWidth().padding(12.dp)) {
                    Text(if (tamil) plate.taTitle else plate.enTitle,
                        fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                    Spacer(Modifier.height(9.dp))
                    NativePlate(plate.filename, description = if (tamil) plate.taTitle else plate.enTitle,
                        unavailableMessage = if (tamil) "படம் கிடைக்கவில்லை" else "Diagram unavailable",
                        modifier = Modifier.fillMaxWidth().heightIn(min = 160.dp, max = 300.dp))
                    Spacer(Modifier.height(8.dp))
                    Text(if (tamil) plate.taCap else plate.enCap, fontSize = 13.sp)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.ZoomIn, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Text(if (tamil) "பெரிதாக்குக" else "View labelled plate", fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(start = 5.dp))
                    }
                }
            }
        }
        item(key = "misconception") {
            SectionCard(if (tamil) "கவனிக்க வேண்டிய கருத்து" else "Common misconception",
                if (tamil) chapter.misTa else chapter.misEn, Color(0xFFFFF4D8))
        }
        item(key = "activity") {
            SectionCard(if (tamil) "வகுப்பறைச் செயல்பாடு" else "Classroom application",
                if (tamil) chapter.activityTa else chapter.activityEn, Color(0xFFE8F5ED))
        }
        item(key = "status") {
            ElevatedCard {
                Row(Modifier.fillMaxWidth().clickable { onCompleted(!completed) }.padding(18.dp),
                    verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = completed, onCheckedChange = { onCompleted(it) },
                        modifier = Modifier.testTag("completionToggle"))
                    Spacer(Modifier.width(8.dp))
                    Text(if (tamil) "இந்தப் பாடத்தை முடித்துவிட்டேன்" else "Mark this chapter as completed",
                        modifier = Modifier.weight(1f), fontWeight = FontWeight.SemiBold)
                }
            }
        }
        item(key = "pagination") {
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(onClick = { onChapter(chapterList[index - 1]) }, enabled = index > 0,
                    modifier = Modifier.weight(1f)) { Text(if (tamil) "← முந்தையது" else "← Previous") }
                Button(onClick = { onChapter(chapterList[index + 1]) },
                    enabled = index < chapterList.lastIndex, modifier = Modifier.weight(1f)) {
                    Text(if (tamil) "அடுத்தது →" else "Next →")
                }
            }
        }
    }
    expanded?.let { plate -> PlateDialog(plate, tamil, onClose = { expanded = null }) }
}

@Composable
private fun SectionCard(title: String, body: String, background: Color) {
    Surface(color = background, contentColor = Navy, shape = RoundedCornerShape(14.dp)) {
        Column(Modifier.fillMaxWidth().padding(17.dp)) {
            Text(title, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Spacer(Modifier.height(7.dp))
            Text(body, lineHeight = 23.sp, fontSize = 14.sp)
        }
    }
}

/** Renders semantic formatted lesson text with a real Android TextView. No HTML page or browser. */
@Composable
private fun NativeRichText(html: String, size: Float) {
    val color = MaterialTheme.colorScheme.onSurface
    AndroidView(
        factory = { context -> TextView(context).apply {
            setTextIsSelectable(true)
            setLineSpacing(6f, 1.12f)
            linksClickable = true
            movementMethod = LinkMovementMethod.getInstance()
            setPadding(0, 0, 0, 4)
        } },
        update = { view ->
            view.text = Html.fromHtml(html, Html.FROM_HTML_MODE_COMPACT)
            view.setTextSize(TypedValue.COMPLEX_UNIT_SP, size)
            view.setTextColor(android.graphics.Color.argb((color.alpha * 255).roundToInt(),
                (color.red * 255).roundToInt(), (color.green * 255).roundToInt(),
                (color.blue * 255).roundToInt()))
        }, modifier = Modifier.fillMaxWidth()
    )
}

@Composable
private fun NativePlate(file: String, description: String, unavailableMessage: String, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val bitmap = remember(file) {
        runCatching { context.assets.open("plates/$file").use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
    }
    Box(modifier.background(Color(0xFFFAFCFD), RoundedCornerShape(10.dp)), contentAlignment = Alignment.Center) {
        if (bitmap != null) {
            Image(bitmap = bitmap, contentDescription = description,
                modifier = Modifier.fillMaxWidth().padding(4.dp), contentScale = ContentScale.Fit)
        } else {
            Text("$unavailableMessage: $file", color = Color.Red)
        }
    }
}

@Composable
private fun PlateDialog(plate: TeachingPlate, tamil: Boolean, onClose: () -> Unit) {
    var zoom by remember(plate.id) { mutableFloatStateOf(1f) }
    var pan by remember(plate.id) { mutableStateOf(Offset.Zero) }
    val context = LocalContext.current
    val bitmap = remember(plate.filename) {
        runCatching { context.assets.open("plates/${plate.filename}").use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
    }
    Dialog(onDismissRequest = onClose, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(modifier = Modifier.fillMaxSize().testTag("plateDialog"), color = MaterialTheme.colorScheme.surface) {
            Column {
                Row(modifier = Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text(if (tamil) plate.taTitle else plate.enTitle, modifier = Modifier.weight(1f),
                        fontWeight = FontWeight.Bold, fontSize = 17.sp, maxLines = 2)
                    IconButton(onClick = onClose) {
                        Icon(Icons.Default.Close, contentDescription = if (tamil) "படத்தை மூடுக" else "Close image")
                    }
                }
                Box(Modifier.fillMaxWidth().weight(1f).background(Color.White)
                    .pointerInput(plate.id) {
                        detectTransformGestures { _, drag, magnification, _ ->
                            zoom = (zoom * magnification).coerceIn(1f, 5f)
                            pan = if (zoom <= 1.01f) Offset.Zero else pan + drag
                        }
                    }
                    .pointerInput(plate.id) {
                        detectTapGestures(onDoubleTap = {
                            zoom = if (zoom > 1f) 1f else 2.5f
                            pan = Offset.Zero
                        })
                    }, contentAlignment = Alignment.Center) {
                    if (bitmap != null) Image(bitmap = bitmap,
                        contentDescription = if (tamil) plate.taTitle else plate.enTitle,
                        contentScale = ContentScale.Fit,
                        modifier = Modifier.fillMaxSize().graphicsLayer {
                            scaleX = zoom
                            scaleY = zoom
                            translationX = pan.x
                            translationY = pan.y
                        })
                }
                Text(if (tamil) plate.taCap else plate.enCap,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp), fontSize = 13.sp)
                OutlinedButton(onClick = { zoom = 1f; pan = Offset.Zero },
                    modifier = Modifier.align(Alignment.CenterHorizontally).padding(bottom = 14.dp)) {
                    Icon(Icons.Default.CenterFocusStrong, contentDescription = null)
                    Spacer(Modifier.width(5.dp))
                    Text(if (tamil) "அசல் அளவு" else "Reset zoom")
                }
            }
        }
    }
}

/** Native assessment screen; selections and scoring run in Kotlin, never JavaScript. */
@Composable
private fun QuestionScreen(banks: Map<Int, QuestionBank>, tamil: Boolean, selectedUnit: Int,
    onUnit: (Int) -> Unit, modifier: Modifier = Modifier) {
    var part by rememberSaveable { mutableStateOf("A") }
    val context = LocalContext.current
    val quizPrefs = remember(context) {
        context.getSharedPreferences("native_intro_zoology_quiz_v1", Context.MODE_PRIVATE)
    }
    val answerKey = "unit_${selectedUnit}_${part}_answers"
    val submittedKey = "unit_${selectedUnit}_${part}_submitted"
    // A fresh Activity has a fresh composition. Restore draft answers from
    // durable Android preferences instead of relying on nested Compose saves.
    val answers = remember(selectedUnit, part) {
        mutableStateMapOf<Int, Int>().apply {
            quizPrefs.getString(answerKey, "").orEmpty().split(',')
                .filter { it.isNotBlank() }.forEach { record ->
                    val pair = record.split(':', limit = 2)
                    if (pair.size == 2) {
                        val index = pair[0].toIntOrNull()
                        val option = pair[1].toIntOrNull()
                        if (index != null && option != null && index >= 0 && option in 0..3) {
                            this[index] = option
                        }
                    }
                }
        }
    }
    var submitted by remember(selectedUnit, part) {
        mutableStateOf(quizPrefs.getBoolean(submittedKey, false))
    }
    fun recordAnswer(index: Int, option: Int) {
        answers[index] = option
        quizPrefs.edit().putString(
            answerKey, answers.entries.sortedBy { it.key }
                .joinToString(",") { "${it.key}:${it.value}" }
        ).apply()
    }
    val b = banks.getValue(selectedUnit)
    val mcqs = if (tamil) b.mcqTa else b.mcqEn
    val prompts = if (part == "B") if (tamil) b.shortTa else b.shortEn
                  else if (tamil) b.longTa else b.longEn
    val correct = mcqs.indices.count { answers[it] == mcqs[it].answer }
    Column(modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Column(Modifier.fillMaxWidth().padding(14.dp)) {
            Text(if (tamil) "அலகுவாரி வினா வங்கி" else "Unit-wise assessment",
                fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Text(if (tamil) "${banks.values.sumOf { it.mcqTa.size }} பல்தேர்வு · ${banks.values.sumOf { it.shortTa.size }} குறுவினா · ${banks.values.sumOf { it.longTa.size }} விரிவான வினா"
                 else "${banks.values.sumOf { it.mcqEn.size }} MCQs · ${banks.values.sumOf { it.shortEn.size }} short-answer · ${banks.values.sumOf { it.longEn.size }} long-answer prompts", fontSize = 12.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(8.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(5.dp)) {
                (1..5).forEach { id ->
                    FilterChip(selected = selectedUnit == id, onClick = { onUnit(id) },
                        label = { Text("$id") }, modifier = Modifier.weight(1f))
                }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                listOf("A", "B", "C").forEach { name ->
                    FilterChip(selected = part == name, onClick = { part = name },
                        label = { Text("Part $name") }, modifier = Modifier.weight(1f))
                }
            }
        }
        LazyColumn(
            modifier = Modifier.fillMaxWidth().weight(1f).testTag("quizScroller"),
            contentPadding = PaddingValues(horizontal = 14.dp, vertical = 6.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (part == "A") {
                item {
                    Text(if (tamil) "சரியான விடையைத் தேர்வு செய்து மதிப்பெண்ணைக் காண்க."
                         else "Choose one answer for each question, then submit your responses.",
                        fontSize = 13.sp)
                }
                items(mcqs.size) { i ->
                    val q = mcqs[i]
                    Card {
                        Column(Modifier.fillMaxWidth().padding(14.dp)) {
                            Text("${i + 1}. ${q.question}", fontWeight = FontWeight.SemiBold,
                                lineHeight = 23.sp)
                            q.options.forEachIndexed { idx, answer ->
                                Row(Modifier.fillMaxWidth().clickable(enabled = !submitted) { recordAnswer(i, idx) }
                                    .padding(vertical = 2.dp), verticalAlignment = Alignment.CenterVertically) {
                                    RadioButton(selected = answers[i] == idx,
                                        modifier = Modifier.testTag("quiz-answer-$i-$idx"),
                                        onClick = { if (!submitted) recordAnswer(i, idx) },
                                        enabled = !submitted)
                                    Text("${'A' + idx}. $answer", fontSize = 14.sp,
                                        color = if (submitted && idx == q.answer) Green
                                                else MaterialTheme.colorScheme.onSurface)
                                }
                            }
                            if (submitted) {
                                Text("${if (tamil) "சரியான விடை" else "Correct answer"}: ${'A' + q.answer}",
                                    color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                if (q.rationale.isNotBlank()) Text(q.rationale, modifier = Modifier.padding(top = 5.dp),
                                    fontSize = 14.sp, lineHeight = 21.sp)
                            }
                        }
                    }
                }
                item {
                    if (!submitted) Button(onClick = {
                        submitted = true
                        quizPrefs.edit().putBoolean(submittedKey, true).apply()
                    },
                        enabled = answers.size == mcqs.size, modifier = Modifier.fillMaxWidth()) {
                        Text(if (tamil) "மதிப்பீட்டை முடிக்க" else "Submit all answers (${answers.size}/${mcqs.size})")
                    } else {
                        Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)) {
                            Column(Modifier.fillMaxWidth().padding(18.dp)) {
                                Text("${if (tamil) "மதிப்பெண்" else "Score"}: $correct / ${mcqs.size}",
                                    fontSize = 21.sp, fontWeight = FontWeight.Bold)
                                Text(if (tamil) "விடைகளை மீண்டும் படித்து திருத்திக் கொள்ளுங்கள்."
                                    else "Review your responses against the highlighted correct answers.")
                                TextButton(onClick = {
                                    answers.clear()
                                    submitted = false
                                    quizPrefs.edit().remove(answerKey).remove(submittedKey).apply()
                                }) {
                                    Text(if (tamil) "மீண்டும் முயற்சி" else "Retake quiz")
                                }
                            }
                        }
                    }
                }
            } else {
                item { Text(if (tamil) "இவை விவாதம் மற்றும் எழுத்துத் தேர்வுப் பயிற்சிக்கான வினாக்கள்."
                    else "Use these prompts for written answers or classroom discussion.", fontSize = 13.sp) }
                items(prompts.size) { i ->
                    Card {
                        Row(Modifier.fillMaxWidth().padding(16.dp)) {
                            Text("${i + 1}.", fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(8.dp))
                            Text(prompts[i], modifier = Modifier.weight(1f), lineHeight = 23.sp)
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(25.dp)) }
        }
    }
}
