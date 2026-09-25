package it.fm.spese

import android.content.Context
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.filled.ReceiptLong
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.AccountBalanceWallet
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.CalendarMonth
import androidx.compose.material.icons.filled.CardGiftcard
import androidx.compose.material.icons.filled.Category
import androidx.compose.material.icons.filled.DeleteForever
import androidx.compose.material.icons.filled.DeleteOutline
import androidx.compose.material.icons.filled.DirectionsBus
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.FileDownload
import androidx.compose.material.icons.filled.FileUpload
import androidx.compose.material.icons.filled.Fingerprint
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.LocalHospital
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.PieChart
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.filled.Restaurant
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.FloatingActionButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.TabRowDefaults
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import org.xmlpull.v1.XmlPullParser
import org.kxml2.io.KXmlParser
import java.io.ByteArrayInputStream
import java.io.InputStream
import java.text.NumberFormat
import java.util.Locale
import java.util.zip.ZipInputStream

// Theme Color Palette
private val Terracotta = Color(0xFFD95D39)
private val Sage = Color(0xFF5B7B68)
private val Ochre = Color(0xFFD99B26)
private val Rose = Color(0xFFC8527A)
private val Violet = Color(0xFF6C5CE7)

data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)

data class CategoryMeta(
    val name: String,
    val color: Color,
    val icon: ImageVector
)

val allCategories = listOf(
    "Spesa",
    "Trasporti",
    "Bar / Ristoranti / Uscite",
    "Mediche",
    "Fitto / Bollette / Casa",
    "Regali",
    "Ricorrenti",
    "Altro"
)

fun getCategoryMeta(category: String): CategoryMeta {
    val norm = category.lowercase(Locale.ITALY).trim()
    return when {
        norm.contains("spesa") -> CategoryMeta("Spesa", Sage, Icons.Default.ShoppingCart)
        norm.contains("trasport") -> CategoryMeta("Trasporti", Color(0xFF3B82F6), Icons.Default.DirectionsBus)
        norm.contains("bar") || norm.contains("ristorant") || norm.contains("uscit") || norm.contains("locali") -> CategoryMeta("Bar / Ristoranti / Uscite", Ochre, Icons.Default.Restaurant)
        norm.contains("medic") || norm.contains("salute") || norm.contains("farmac") -> CategoryMeta("Mediche", Color(0xFF10B981), Icons.Default.LocalHospital)
        norm.contains("fitto") || norm.contains("bollett") || norm.contains("casa") -> CategoryMeta("Fitto / Bollette / Casa", Terracotta, Icons.Default.Home)
        norm.contains("regal") -> CategoryMeta("Regali", Rose, Icons.Default.CardGiftcard)
        norm.contains("ricorrent") || norm.contains("abbonament") -> CategoryMeta("Ricorrenti", Violet, Icons.Default.Repeat)
        else -> CategoryMeta(category.ifBlank { "Altro" }, Color(0xFF8B95A5), Icons.Default.Category)
    }
}

fun extractYear(month: String): String {
    val digits = month.filter { it.isDigit() }
    return when {
        digits.length == 4 -> digits
        digits.length == 2 -> "20$digits"
        else -> "2026"
    }
}

private fun formatAmount(value: Double, isPrivacyMode: Boolean): String {
    return if (isPrivacyMode) "•••• €" else NumberFormat.getCurrencyInstance(Locale.ITALY).format(value)
}

fun parseAmount(raw: String?): Double? {
    if (raw.isNullOrBlank()) return null
    var cleaned = raw.trim()
        .replace("€", "")
        .replace(" ", "")
        .replace("\u00A0", "")
        .replace("\"", "")
        .removePrefix("\uFEFF")

    if (cleaned.isBlank()) return null

    val lastDot = cleaned.lastIndexOf('.')
    val lastComma = cleaned.lastIndexOf(',')

    cleaned = if (lastDot != -1 && lastComma != -1) {
        if (lastComma > lastDot) {
            cleaned.replace(".", "").replace(',', '.')
        } else {
            cleaned.replace(",", "")
        }
    } else if (lastComma != -1) {
        cleaned.replace(',', '.')
    } else {
        cleaned
    }

    return cleaned.toDoubleOrNull()
}

/**
 * Parser intelligente per inserimento spese con Linguaggio Naturale (IA locale).
 */
data class ParsedAiExpense(
    val title: String,
    val category: String,
    val amount: Double?
)

object AiExpenseParser {

    fun parseText(input: String): ParsedAiExpense {
        if (input.isBlank()) return ParsedAiExpense("", "Altro", null)

        val amount = extractAmount(input)
        val category = detectCategory(input)
        val title = cleanTitle(input)

        return ParsedAiExpense(
            title = title.ifBlank { "Spesa" },
            category = category,
            amount = amount
        )
    }

    private fun extractAmount(text: String): Double? {
        val regex = Regex("""(?i)(\d+[.,]\d{1,2}|\d+)\s*(?:€|euro)?""")
        val matches = regex.findAll(text)

        for (match in matches) {
            val candidate = match.value
            val parsed = parseAmount(candidate)
            if (parsed != null && parsed > 0) {
                return parsed
            }
        }
        return null
    }

    private fun detectCategory(text: String): String {
        val norm = text.lowercase(Locale.ITALY)
        return when {
            norm.contains("spesa") || norm.contains("supermercato") || norm.contains("conad") || norm.contains("coop") || norm.contains("esselunga") || norm.contains("alimenta") -> "Spesa"
            norm.contains("bar") || norm.contains("ristorante") || norm.contains("pizzeria") || norm.contains("caffè") || norm.contains("caffe") || norm.contains("cornetto") || norm.contains("pub") || norm.contains("pranzo") || norm.contains("cena") || norm.contains("aperitivo") -> "Bar / Ristoranti / Uscite"
            norm.contains("trasport") || norm.contains("taxi") || norm.contains("bus") || norm.contains("metro") || norm.contains("treno") || norm.contains("benzina") || norm.contains("carburante") || norm.contains("autostrada") || norm.contains("uber") -> "Trasporti"
            norm.contains("farmacia") || norm.contains("medico") || norm.contains("mediche") || norm.contains("dottore") || norm.contains("dentista") || norm.contains("sciroppo") || norm.contains("salute") -> "Mediche"
            norm.contains("fitto") || norm.contains("affitto") || norm.contains("bolletta") || norm.contains("luce") || norm.contains("gas") || norm.contains("acqua") || norm.contains("enel") || norm.contains("internet") || norm.contains("casa") -> "Fitto / Bollette / Casa"
            norm.contains("regalo") || norm.contains("compleanno") || norm.contains("pensiero") -> "Regali"
            norm.contains("abbonamento") || norm.contains("spotify") || norm.contains("netflix") || norm.contains("palestra") || norm.contains("ricorrente") -> "Ricorrenti"
            else -> "Altro"
        }
    }

    private fun cleanTitle(text: String): String {
        var clean = text
            .replace(Regex("""(?i)(ho speso|spesi|spesa di|pagato|pagati|per)"""), "")
            .replace(Regex("""(?i)\d+[.,]\d{1,2}\s*(?:€|euro)?"""), "")
            .replace(Regex("""(?i)\d+\s*(?:€|euro)"""), "")
            .replace(Regex("""[€]"""), "")
            .trim()

        clean = clean.replace(Regex("""\s+"""), " ")
            .lowercase(Locale.ITALY)
            .replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.ITALY) else it.toString() }

        return clean
    }
}

private const val ExpenseStore = "expense_store"

private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val category = parts[1]
            val amount = parseAmount(parts[2]) ?: return@mapNotNull null
            val month = if (parts.size >= 4) parts[3] else "settembre 26"
            Expense(title, category, amount, month)
        } else null
    }
}

private fun saveExpenses(context: Context, expenses: List<Expense>) {
    val raw = expenses.joinToString("\n") { "${it.title}\t${it.category}\t${it.amount}\t${it.month}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}

private fun clearAllData(context: Context) {
    context.getSharedPreferences(ExpenseStore, 0).edit().clear().putString("items", "").apply()
}

private fun loadBudget(context: Context): Double {
    val valStr = context.getSharedPreferences(ExpenseStore, 0).getString("monthly_budget", null)
    return parseAmount(valStr) ?: 2000.0
}

private fun saveBudget(context: Context, budget: Double?) {
    val prefs = context.getSharedPreferences(ExpenseStore, 0).edit()
    if (budget != null) {
        prefs.putString("monthly_budget", budget.toString())
    } else {
        prefs.remove("monthly_budget")
    }
    prefs.apply()
}

private fun loadPrivacyMode(context: Context): Boolean {
    return context.getSharedPreferences(ExpenseStore, 0).getBoolean("privacy_mode", true)
}

private fun savePrivacyMode(context: Context, enabled: Boolean) {
    context.getSharedPreferences(ExpenseStore, 0).edit().putBoolean("privacy_mode", enabled).apply()
}

private fun loadIsFirstLaunch(context: Context): Boolean {
    return context.getSharedPreferences(ExpenseStore, 0).getBoolean("is_first_launch", true)
}

private fun saveIsFirstLaunch(context: Context, isFirst: Boolean) {
    context.getSharedPreferences(ExpenseStore, 0).edit().putBoolean("is_first_launch", isFirst).apply()
}

private fun exportExpensesToCsv(context: Context, uri: Uri, expenses: List<Expense>): Boolean {
    return try {
        context.contentResolver.openOutputStream(uri)?.use { outputStream ->
            outputStream.bufferedWriter().use { writer ->
                writer.write("Mese,Descrizione,Categoria,Importo\n")
                expenses.forEach { expense ->
                    writer.write("\"${expense.month}\",\"${expense.title.replace("\"", "\"\"")}\",\"${expense.category}\",${expense.amount}\n")
                }
            }
        }
        true
    } catch (e: Exception) {
        e.printStackTrace()
        false
    }
}

class MainActivity : FragmentActivity() {

    private lateinit var importLauncher: ActivityResultLauncher<Array<String>>
    private lateinit var exportLauncher: ActivityResultLauncher<String>

    private var onImportResult: ((Uri?) -> Unit)? = null
    private var onExportResult: ((Uri?) -> Unit)? = null

    override fun onResume() {
        super.onResume()
        savePrivacyMode(this, true)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        importLauncher = registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
            onImportResult?.invoke(uri)
        }
        
        exportLauncher = registerForActivityResult(ActivityResultContracts.CreateDocument("text/csv")) { uri ->
            onExportResult?.invoke(uri)
        }
        
        setContent {
            SpeseAppWithSecurity(
                activity = this,
                launchImport = { callback ->
                    onImportResult = callback
                    importLauncher.launch(arrayOf("*/*"))
                },
                launchExport = { filename, callback ->
                    onExportResult = callback
                    exportLauncher.launch(filename)
                }
            )
        }
    }
}

@Composable
private fun SpeseAppWithSecurity(
    activity: FragmentActivity,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit)
) {
    val isDarkTheme = isSystemInDarkTheme()
    var isUnlocked by remember { mutableStateOf(false) }

    fun triggerBiometric() {
        launchBiometricPrompt(
            activity = activity,
            onSuccess = { isUnlocked = true },
            onError = { msg ->
                Toast.makeText(activity, msg, Toast.LENGTH_SHORT).show()
            }
        )
    }

    LaunchedEffect(Unit) {
        triggerBiometric()
    }

    if (!isUnlocked) {
        SecurityLockOverlay(
            isDarkTheme = isDarkTheme,
            onUnlockClick = { triggerBiometric() }
        )
    } else {
        SpeseApp(
            onLockClick = { isUnlocked = false },
            launchImport = launchImport,
            launchExport = launchExport
        )
    }
}

private fun launchBiometricPrompt(
    activity: FragmentActivity,
    onSuccess: () -> Unit,
    onError: (String) -> Unit
) {
    val executor = ContextCompat.getMainExecutor(activity)
    val biometricPrompt = BiometricPrompt(
        activity,
        executor,
        object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                super.onAuthenticationSucceeded(result)
                onSuccess()
            }

            override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                super.onAuthenticationError(errorCode, errString)
                onError(errString.toString())
            }

            override fun onAuthenticationFailed() {
                super.onAuthenticationFailed()
                onError("Autenticazione non riuscita.")
            }
        }
    )

    val promptInfo = BiometricPrompt.PromptInfo.Builder()
        .setTitle("Accesso Sicuro Spese")
        .setSubtitle("Autenticati con l'impronta digitale o la biometria")
        .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL)
        .build()

    try {
        biometricPrompt.authenticate(promptInfo)
    } catch (e: Exception) {
        e.printStackTrace()
        onError("Biometria non disponibile sul dispositivo.")
    }
}

@Composable
private fun SecurityLockOverlay(
    isDarkTheme: Boolean,
    onUnlockClick: () -> Unit
) {
    val bgColor = if (isDarkTheme) Color(0xFF121110) else Color(0xFFFAF7F2)
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .padding(32.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Box(
                modifier = Modifier
                    .size(96.dp)
                    .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(72.dp)
                        .background(Terracotta, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Lock,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(36.dp)
                    )
                }
            }

            Spacer(Modifier.height(24.dp))

            Text(
                "App Bloccata",
                color = textColor,
                fontSize = 26.sp,
                fontWeight = FontWeight.ExtraBold
            )

            Spacer(Modifier.height(8.dp))

            Text(
                "I tuoi dati finanziari sono protetti con la sicurezza biometrica.",
                color = Sage,
                fontSize = 14.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 16.dp)
            )

            Spacer(Modifier.height(36.dp))

            Button(
                onClick = onUnlockClick,
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = Terracotta),
                modifier = Modifier.height(56.dp).fillMaxWidth(0.85f)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Fingerprint,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.width(12.dp))
                    Text("Sblocca con Impronta", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
private fun SpeseApp(
    onLockClick: () -> Unit,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit)
) {
    val context = LocalContext.current
    val isDarkTheme = isSystemInDarkTheme()

    val paperColor = if (isDarkTheme) Color(0xFF121110) else Color(0xFFFAF7F2)
    val cardBgColor = if (isDarkTheme) Color(0xFF1E1C1A) else Color.White
    val subTextColor = if (isDarkTheme) Color(0xFFA0B2A3) else Color(0xFF5B7B68)

    var showTutorial by remember { mutableStateOf(loadIsFirstLaunch(context)) }
    var selectedTab by remember { mutableStateOf(0) }
    var expenses by remember { mutableStateOf(loadExpenses(context)) }
    var monthlyBudget by remember { mutableStateOf<Double?>(loadBudget(context)) }
    var isPrivacyMode by remember { mutableStateOf(loadPrivacyMode(context)) }

    var showAddDialog by remember { mutableStateOf(false) }
    var showBudgetDialog by remember { mutableStateOf(false) }
    var showClearConfirmDialog by remember { mutableStateOf(false) }

    var selectedCategoryFilter by remember { mutableStateOf<String?>(null) }
    var selectedMonthFilter by remember { mutableStateOf<String?>(null) }

    val availableMonths = remember(expenses) {
        val list = expenses.map { it.month }.distinct()
        if (list.isEmpty()) listOf("settembre 26") else list
    }

    val activeMonthExpenses = remember(expenses, selectedMonthFilter) {
        if (selectedMonthFilter.isNullOrBlank()) {
            expenses
        } else {
            expenses.filter { it.month.equals(selectedMonthFilter, ignoreCase = true) }
        }
    }

    val activeNumMonths = remember(activeMonthExpenses) {
        activeMonthExpenses.map { it.month }.distinct().size.coerceAtLeast(1)
    }

    val total = activeMonthExpenses.sumOf { it.amount }

    MaterialTheme {
        if (showTutorial) {
            OnboardingTutorial(
                isDarkTheme = isDarkTheme,
                onFinish = {
                    saveIsFirstLaunch(context, false)
                    showTutorial = false
                }
            )
        } else {
            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                Scaffold(
                    containerColor = Color.Transparent,
                    floatingActionButton = {
                        FloatingActionButton(
                            onClick = { showAddDialog = true },
                            shape = CircleShape,
                            containerColor = Terracotta,
                            contentColor = Color.White,
                            elevation = FloatingActionButtonDefaults.elevation(
                                defaultElevation = 8.dp,
                                pressedElevation = 12.dp
                            ),
                            modifier = Modifier
                                .size(62.dp)
                                .shadow(12.dp, CircleShape, spotColor = Terracotta)
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Aggiungi spesa", modifier = Modifier.size(30.dp))
                        }
                    },
                    bottomBar = {
                        Surface(
                            shadowElevation = 16.dp,
                            color = cardBgColor,
                            shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
                        ) {
                            NavigationBar(
                                containerColor = cardBgColor,
                                tonalElevation = 0.dp,
                                windowInsets = WindowInsets.navigationBars,
                                modifier = Modifier.height(82.dp)
                            ) {
                                listOf(
                                    "Home" to Icons.Default.Home,
                                    "Movimenti" to Icons.AutoMirrored.Filled.ReceiptLong,
                                    "Report" to Icons.Default.BarChart
                                ).forEachIndexed { index, item ->
                                    val selected = selectedTab == index
                                    NavigationBarItem(
                                        selected = selected,
                                        onClick = { selectedTab = index },
                                        icon = {
                                            Icon(
                                                imageVector = item.second,
                                                contentDescription = item.first,
                                                modifier = Modifier.size(24.dp)
                                            )
                                        },
                                        label = {
                                            Text(
                                                text = item.first,
                                                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                                                fontSize = 12.sp
                                            )
                                        },
                                        colors = NavigationBarItemDefaults.colors(
                                            selectedIconColor = Terracotta,
                                            selectedTextColor = Terracotta,
                                            indicatorColor = Terracotta.copy(alpha = 0.16f),
                                            unselectedIconColor = subTextColor,
                                            unselectedTextColor = subTextColor
                                        )
                                    )
                                }
                            }
                        }
                    }
                ) { padding ->
                    when (selectedTab) {
                        0 -> Dashboard(
                            expenses = activeMonthExpenses,
                            total = total,
                            budget = monthlyBudget,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onTogglePrivacy = {
                                isPrivacyMode = !isPrivacyMode
                                savePrivacyMode(context, isPrivacyMode)
                                Toast.makeText(context, if (isPrivacyMode) "Cifre nascoste" else "Cifre visibili", Toast.LENGTH_SHORT).show()
                            },
                            onLockClick = onLockClick,
                            onOpenTutorialClick = { showTutorial = true },
                            onMonthSelect = { selectedMonthFilter = it },
                            onCategoryClick = { cat ->
                                selectedCategoryFilter = cat
                                selectedTab = 1
                            },
                            onImportClick = {
                                launchImport { uri ->
                                    if (uri != null) {
                                        val imported = XlsSheetImporter.importFromUri(context, uri)
                                        if (imported.isNotEmpty()) {
                                            expenses = imported + expenses
                                            saveExpenses(context, expenses)
                                            selectedMonthFilter = imported.firstOrNull()?.month ?: selectedMonthFilter
                                            Toast.makeText(context, "Importati con successo ${imported.size} movimenti!", Toast.LENGTH_LONG).show()
                                        } else {
                                            Toast.makeText(context, "Nessun movimento valido trovato nel file.", Toast.LENGTH_LONG).show()
                                        }
                                    }
                                }
                            },
                            onExportClick = {
                                launchExport("spese_backup.csv") { uri ->
                                    if (uri != null) {
                                        val ok = exportExpensesToCsv(context, uri, expenses)
                                        if (ok) {
                                            Toast.makeText(context, "File CSV esportato con successo!", Toast.LENGTH_LONG).show()
                                        } else {
                                            Toast.makeText(context, "Errore durante l'esportazione.", Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                }
                            },
                            onClearAllClick = { showClearConfirmDialog = true },
                            onSetBudgetClick = { showBudgetDialog = true },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )
                        1 -> Movements(
                            expenses = activeMonthExpenses,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            initialCategoryFilter = selectedCategoryFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            onClearCategoryFilter = { selectedCategoryFilter = null },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )
                        else -> Reports(
                            allExpenses = expenses,
                            filteredExpenses = activeMonthExpenses,
                            total = total,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            modifier = Modifier.padding(padding)
                        )
                    }
                }
            }
        }
    }

    if (showAddDialog) {
        AddExpenseDialog(
            currentMonth = selectedMonthFilter ?: availableMonths.firstOrNull() ?: "settembre 26",
            isDarkTheme = isDarkTheme,
            onDismiss = { showAddDialog = false },
            onAdd = { expense ->
                expenses = listOf(expense) + expenses
                saveExpenses(context, expenses)
                showAddDialog = false
            }
        )
    }

    if (showBudgetDialog) {
        SetBudgetDialog(
            currentBudget = monthlyBudget,
            isDarkTheme = isDarkTheme,
            onDismiss = { showBudgetDialog = false },
            onSave = { newBudget ->
                monthlyBudget = newBudget
                saveBudget(context, newBudget)
                showBudgetDialog = false
                Toast.makeText(context, "Budget aggiornato!", Toast.LENGTH_SHORT).show()
            }
        )
    }

    if (showClearConfirmDialog) {
        val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
        val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White

        AlertDialog(
            onDismissRequest = { showClearConfirmDialog = false },
            shape = RoundedCornerShape(32.dp),
            containerColor = dialogBg,
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.DeleteForever, contentDescription = null, tint = Terracotta)
                    }
                    Spacer(Modifier.width(12.dp))
                    Text("Cancella tutti i dati", color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                }
            },
            text = {
                Text(
                    "Sei sicuro di voler eliminare definitivamente tutte le spese registrate nell'app? L'operazione non può essere annullata.",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 14.sp
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        clearAllData(context)
                        expenses = emptyList()
                        selectedMonthFilter = null
                        showClearConfirmDialog = false
                        Toast.makeText(context, "Tutti i dati sono stati cancellati!", Toast.LENGTH_LONG).show()
                    },
                    shape = CircleShape,
                    colors = ButtonDefaults.buttonColors(containerColor = Terracotta)
                ) {
                    Text("Cancella tutto", fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 8.dp))
                }
            },
            dismissButton = {
                TextButton(onClick = { showClearConfirmDialog = false }, shape = CircleShape) {
                    Text("Annulla", color = Sage)
                }
            }
        )
    }
}

data class TutorialStep(
    val title: String,
    val description: String,
    val icon: ImageVector,
    val color: Color
)

@Composable
private fun OnboardingTutorial(
    isDarkTheme: Boolean,
    onFinish: () -> Unit
) {
    var currentStep by remember { mutableStateOf(0) }
    val totalSteps = 5

    val bgColor = if (isDarkTheme) Color(0xFF121110) else Color(0xFFFAF7F2)
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDarkTheme) Color(0xFFA0B2A3) else Color(0xFF5B7B68)

    val stepData = listOf(
        TutorialStep(
            title = "Benvenuto in Spese FM",
            description = "Piattaforma moderna e circolare per gestire le tue uscite. Per la tua riservatezza, la Modalità Privacy è attiva di default al primo avvio.",
            icon = Icons.Default.AccountBalanceWallet,
            color = Terracotta
        ),
        TutorialStep(
            title = "Modalità Privacy Protetta",
            description = "Le cifre sono nascoste (•••• €). Usa il pulsante ben visibile 'Nascosto / Visibile' in alto a destra nella schermata principale per mostrare o nascondere gli importi.",
            icon = Icons.Default.VisibilityOff,
            color = Ochre
        ),
        TutorialStep(
            title = "Importazione Excel e CSV",
            description = "Importa al volo i tuoi file .xlsx o .csv con rilevamento automatico delle colonne, delle note e dei formati bancari.",
            icon = Icons.Default.FileUpload,
            color = Sage
        ),
        TutorialStep(
            title = "Sicurezza Biometrica",
            description = "I tuoi dati finanziari restano al 100% protetti sul tuo dispositivo, tutelati dall'impronta digitale o riconoscimento facciale.",
            icon = Icons.Default.Fingerprint,
            color = Violet
        ),
        TutorialStep(
            title = "Report & Budget Mensile",
            description = "Analizza i grafici a ciambella per categorie, imposta il tuo tetto di spesa mensile e consulta le medie storiche.",
            icon = Icons.Default.BarChart,
            color = Rose
        )
    )

    val current = stepData[currentStep]

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .padding(24.dp)
    ) {
        // Skip Button top right
        Row(
            modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(8.dp).background(Terracotta, CircleShape))
                Spacer(Modifier.width(8.dp))
                Text("GUIDA ${currentStep + 1}/$totalSteps", color = Terracotta, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }

            if (currentStep < totalSteps - 1) {
                TextButton(onClick = onFinish, shape = CircleShape) {
                    Text("Salta", color = subTextColor, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                }
            }
        }

        // Center Content Slide
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.Center),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(
                modifier = Modifier
                    .size(130.dp)
                    .background(current.color.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(96.dp)
                        .background(current.color, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = current.icon,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(48.dp)
                    )
                }
            }

            Spacer(Modifier.height(32.dp))

            Text(
                current.title,
                color = textColor,
                fontSize = 24.sp,
                fontWeight = FontWeight.ExtraBold,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 16.dp)
            )

            Spacer(Modifier.height(12.dp))

            Text(
                current.description,
                color = subTextColor,
                fontSize = 15.sp,
                textAlign = TextAlign.Center,
                lineHeight = 22.sp,
                modifier = Modifier.padding(horizontal = 20.dp)
            )

            Spacer(Modifier.height(32.dp))

            // Indicator Dots
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                for (i in 0 until totalSteps) {
                    Box(
                        modifier = Modifier
                            .size(if (i == currentStep) 24.dp else 8.dp, 8.dp)
                            .background(
                                if (i == currentStep) current.color else subTextColor.copy(alpha = 0.3f),
                                CircleShape
                            )
                    )
                }
            }
        }

        // Bottom Controls
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
                .padding(bottom = 24.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (currentStep > 0) {
                TextButton(
                    onClick = { currentStep-- },
                    shape = CircleShape
                ) {
                    Text("Indietro", color = subTextColor, fontWeight = FontWeight.Bold)
                }
            } else {
                Spacer(Modifier.width(80.dp))
            }

            Button(
                onClick = {
                    if (currentStep < totalSteps - 1) {
                        currentStep++
                    } else {
                        onFinish()
                    }
                },
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = current.color),
                modifier = Modifier.height(52.dp).padding(horizontal = 16.dp)
            ) {
                Text(
                    if (currentStep == totalSteps - 1) "Inizia subito" else "Avanti",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 8.dp)
                )
            }
        }
    }
}

@Composable
private fun BackgroundCircles(isDark: Boolean) {
    val alphaMultiplier = if (isDark) 0.6f else 1.0f
    Canvas(modifier = Modifier.fillMaxSize()) {
        drawCircle(
            color = Terracotta.copy(alpha = 0.05f * alphaMultiplier),
            radius = 220.dp.toPx(),
            center = Offset(size.width * 0.95f, size.height * 0.08f)
        )
        drawCircle(
            color = Sage.copy(alpha = 0.06f * alphaMultiplier),
            radius = 160.dp.toPx(),
            center = Offset(size.width * 0.05f, size.height * 0.22f)
        )
        drawCircle(
            color = Ochre.copy(alpha = 0.04f * alphaMultiplier),
            radius = 140.dp.toPx(),
            center = Offset(size.width * 0.9f, size.height * 0.65f)
        )
    }
}

@Composable
private fun MonthSelectorStrip(
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    onMonthSelect: (String?) -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White

    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(horizontal = 2.dp)
    ) {
        item {
            val isAllSelected = selectedMonth.isNullOrBlank()
            Surface(
                color = if (isAllSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isAllSelected) 3.dp else 1.dp,
                modifier = Modifier.clip(CircleShape).clickable { onMonthSelect(null) }
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.CalendarMonth,
                        contentDescription = null,
                        tint = if (isAllSelected) Color.White else Terracotta,
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        "Tutti i Mesi",
                        color = if (isAllSelected) Color.White else textColor,
                        fontWeight = if (isAllSelected) FontWeight.Bold else FontWeight.Medium,
                        fontSize = 12.sp
                    )
                }
            }
        }

        items(availableMonths) { monthName ->
            val isSelected = selectedMonth?.equals(monthName, ignoreCase = true) == true
            Surface(
                color = if (isSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isSelected) 3.dp else 1.dp,
                modifier = Modifier.clip(CircleShape).clickable { onMonthSelect(monthName) }
            ) {
                Text(
                    monthName,
                    color = if (isSelected) Color.White else textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    fontSize = 12.sp,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp)
                )
            }
        }
    }
}

@Composable
private fun Dashboard(
    expenses: List<Expense>,
    total: Double,
    budget: Double?,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onTogglePrivacy: () -> Unit,
    onLockClick: () -> Unit,
    onOpenTutorialClick: () -> Unit,
    onMonthSelect: (String?) -> Unit,
    onCategoryClick: (String) -> Unit,
    onImportClick: () -> Unit,
    onExportClick: () -> Unit,
    onClearAllClick: () -> Unit,
    onSetBudgetClick: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)

    LazyColumn(
        modifier = modifier.fillMaxSize().padding(horizontal = 20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Spacer(Modifier.height(8.dp))
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(10.dp).background(Terracotta, CircleShape))
                    Spacer(Modifier.width(8.dp))
                    Text(
                        if (selectedMonth != null) selectedMonth else "$numMonths mesi analizzati",
                        color = Terracotta,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
                Spacer(Modifier.height(2.dp))
                Text("Panoramica Spese", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            }
        }

        if (availableMonths.size > 1) {
            item {
                MonthSelectorStrip(availableMonths, selectedMonth, isDark, onMonthSelect)
            }
        }

        item { SummaryCard(total, budget, expenses, numMonths, isDark, isPrivacyMode, onSetBudgetClick) }

        item {
            QuickActionsStrip(
                isPrivacyMode = isPrivacyMode,
                isDark = isDark,
                onTogglePrivacy = onTogglePrivacy,
                onLockClick = onLockClick,
                onOpenTutorialClick = onOpenTutorialClick,
                onImportClick = onImportClick,
                onExportClick = onExportClick,
                onClearAllClick = onClearAllClick
            )
        }

        item { CategoryQuickStrip(expenses, isDark, isPrivacyMode, onCategoryClick) }

        item { InsightCard(expenses, isDark, isPrivacyMode) }

        item {
            Row(
                modifier = Modifier.fillMaxWidth().padding(top = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Ultimi Movimenti", color = textColor, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Surface(
                    color = if (isDark) Color(0xFF282522) else Color(0xFFEBE5DA),
                    shape = CircleShape,
                    modifier = Modifier.clip(CircleShape).clickable { onCategoryClick("") }
                ) {
                    Text(
                        "Vedi tutte",
                        color = Terracotta,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    )
                }
            }
        }

        if (expenses.isEmpty()) {
            item {
                Box(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier.size(64.dp).background(if (isDark) Color(0xFF282522) else Color(0xFFEBE5DA), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.ReceiptLong, contentDescription = null, tint = Sage, modifier = Modifier.size(32.dp))
                        }
                        Spacer(Modifier.height(12.dp))
                        Text("Nessuna spesa presente", color = textColor, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        Text(
                            "Aggiungi una nuova spesa con il pulsante + oppure importa un file XLS/CSV con lo strumento di importazione.",
                            color = Sage,
                            fontSize = 13.sp,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(horizontal = 24.dp, vertical = 4.dp)
                        )
                    }
                }
            }
        } else {
            items(expenses.take(5)) { ExpenseRow(it, isDark, isPrivacyMode, onDeleteExpense) }
        }

        item { Spacer(Modifier.height(88.dp)) }
    }
}

@Composable
private fun QuickActionsStrip(
    isPrivacyMode: Boolean,
    isDark: Boolean,
    onTogglePrivacy: () -> Unit,
    onLockClick: () -> Unit,
    onOpenTutorialClick: () -> Unit,
    onImportClick: () -> Unit,
    onExportClick: () -> Unit,
    onClearAllClick: () -> Unit
) {
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)

    Column {
        Text("Gestione & Sicurezza", color = textColor, fontSize = 18.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(10.dp))
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(horizontal = 2.dp)
        ) {
            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onTogglePrivacy() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background((if (isPrivacyMode) Ochre else Sage).copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                if (isPrivacyMode) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = null,
                                tint = if (isPrivacyMode) Ochre else Sage,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Privacy", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text(if (isPrivacyMode) "Cifre nascoste" else "Cifre visibili", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }

            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onLockClick() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Lock, contentDescription = null, tint = Terracotta, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Sicurezza", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("Blocca ora", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }

            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onImportClick() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.FileUpload, contentDescription = null, tint = Terracotta, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Importa", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("XLS / CSV", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }

            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onExportClick() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background(Sage.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.FileDownload, contentDescription = null, tint = Sage, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Esporta", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("Backup CSV", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }

            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onOpenTutorialClick() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background(Violet.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null, tint = Violet, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Guida", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("Tutorial app", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }

            item {
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(20.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onClearAllClick() }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(36.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.DeleteForever, contentDescription = null, tint = Terracotta, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text("Svuota", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("Reset dati", color = subTextColor, fontSize = 11.sp)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SummaryCard(
    total: Double,
    budget: Double?,
    expenses: List<Expense>,
    numMonths: Int,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onSetBudgetClick: () -> Unit
) {
    val darkCardBg = if (isDark) Color(0xFF1C1A18) else Color(0xFF282420)

    val monthlyAvg = if (numMonths > 0) total / numMonths else 0.0
    val budgetLimitPerMonth = budget ?: 0.0
    val effectiveBudgetLimit = budgetLimitPerMonth * numMonths

    val budgetPercent = if (effectiveBudgetLimit > 0) ((total / effectiveBudgetLimit) * 100).toInt() else 0
    val budgetRemaining = effectiveBudgetLimit - total

    val ringColor = when {
        effectiveBudgetLimit == 0.0 -> Terracotta
        budgetPercent > 100 -> Terracotta
        budgetPercent > 80 -> Ochre
        else -> Sage
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = darkCardBg),
        shape = RoundedCornerShape(32.dp),
        modifier = Modifier
            .fillMaxWidth()
            .shadow(elevation = 10.dp, shape = RoundedCornerShape(32.dp), spotColor = darkCardBg.copy(alpha = 0.3f))
    ) {
        Box(modifier = Modifier.fillMaxWidth()) {
            Canvas(modifier = Modifier.matchParentSize()) {
                drawCircle(
                    color = ringColor.copy(alpha = 0.08f),
                    radius = 130.dp.toPx(),
                    center = Offset(size.width * 0.85f, size.height * 0.3f)
                )
            }

            Column(Modifier.padding(22.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(modifier = Modifier.size(8.dp).background(ringColor, CircleShape))
                            Spacer(Modifier.width(8.dp))
                            Text(
                                if (numMonths > 1) "TOTALE ($numMonths MESI)" else "TOTALE DEL MESE",
                                color = Color(0xFFC0B8B0),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 1.sp
                            )
                        }
                        Spacer(Modifier.height(6.dp))
                        Text(
                            formatAmount(total, isPrivacyMode),
                            color = Color.White,
                            fontSize = 32.sp,
                            fontWeight = FontWeight.ExtraBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }

                    Spacer(Modifier.width(12.dp))

                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .clip(CircleShape)
                            .clickable { onSetBudgetClick() },
                        contentAlignment = Alignment.Center
                    ) {
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            drawCircle(
                                color = Color.White.copy(alpha = 0.12f),
                                style = Stroke(width = 6.dp.toPx())
                            )
                            val sweep = if (effectiveBudgetLimit > 0) ((total / effectiveBudgetLimit).coerceAtMost(1.0) * 360).toFloat() else 270f
                            drawArc(
                                color = ringColor,
                                startAngle = -90f,
                                sweepAngle = sweep,
                                useCenter = false,
                                style = Stroke(width = 6.dp.toPx(), cap = StrokeCap.Round)
                            )
                        }
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .background(Color.White.copy(alpha = 0.12f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            if (effectiveBudgetLimit > 0) {
                                Text(
                                    if (isPrivacyMode) "••%" else "$budgetPercent%",
                                    color = Color.White,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            } else {
                                Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                            }
                        }
                    }
                }

                Spacer(Modifier.height(18.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(
                        color = Color.White.copy(alpha = 0.08f),
                        shape = CircleShape,
                        modifier = Modifier.weight(1f, fill = false)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier.size(18.dp).background(Sage, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("${expenses.size}", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                            Spacer(Modifier.width(6.dp))
                            Text(
                                if (numMonths > 1) "${formatAmount(monthlyAvg, isPrivacyMode)}/m" else "movimenti",
                                color = Color(0xFFE6DED5),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }

                    Surface(
                        color = ringColor.copy(alpha = 0.22f),
                        shape = CircleShape,
                        modifier = Modifier.clip(CircleShape).clickable { onSetBudgetClick() }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.Edit, contentDescription = null, tint = Color.White, modifier = Modifier.size(12.dp))
                            Spacer(Modifier.width(6.dp))
                            Text(
                                if (effectiveBudgetLimit > 0) {
                                    if (budgetRemaining >= 0) "Rim.: ${formatAmount(budgetRemaining, isPrivacyMode)}" else "Superato!"
                                } else "Budget",
                                color = Color.White,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CategoryQuickStrip(expenses: List<Expense>, isDark: Boolean, isPrivacyMode: Boolean, onCategoryClick: (String) -> Unit) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)

    val categoryTotals = expenses.groupBy { it.category }.mapValues { entry -> entry.value.sumOf { it.amount } }

    Column {
        Text("Categorie principali", color = textColor, fontSize = 18.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(10.dp))
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            contentPadding = PaddingValues(horizontal = 2.dp)
        ) {
            items(allCategories) { category ->
                val meta = getCategoryMeta(category)
                val totalForCat = categoryTotals[category] ?: 0.0

                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(24.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.clip(RoundedCornerShape(24.dp)).clickable { onCategoryClick(category) }
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(38.dp)
                                .background(meta.color.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(meta.icon, contentDescription = null, tint = meta.color, modifier = Modifier.size(18.dp))
                        }
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text(category, color = textColor, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            Text(
                                formatAmount(totalForCat, isPrivacyMode),
                                color = subTextColor,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium,
                                maxLines = 1
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun InsightCard(expenses: List<Expense>, isDark: Boolean, isPrivacyMode: Boolean) {
    val cardBg = if (isDark) Color(0xFF221F1C) else Color(0xFFEFE8DD)
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val top = expenses.groupBy { it.category }.maxByOrNull { entry -> entry.value.sumOf { it.amount } }

    Card(
        colors = CardDefaults.cardColors(containerColor = cardBg),
        shape = RoundedCornerShape(28.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(48.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier.size(36.dp).background(Terracotta, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Lightbulb, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
                }
            }
            Spacer(Modifier.width(16.dp))
            Column(Modifier.weight(1f)) {
                Text("Suggerimento Intelligente", color = textColor, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                Spacer(Modifier.height(2.dp))
                Text(
                    if (top != null) "${top.key} e la spesa maggiore (${formatAmount(top.value.sumOf { it.amount }, isPrivacyMode)}). Prova a fissare un limite mensile!"
                    else "Aggiungi le prime spese per ricevere analisi personalizzate.",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 13.sp,
                    lineHeight = 18.sp
                )
            }
        }
    }
}

@Composable
private fun Movements(
    expenses: List<Expense>,
    availableMonths: List<String>,
    selectedMonth: String?,
    initialCategoryFilter: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onMonthSelect: (String?) -> Unit,
    onClearCategoryFilter: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val softBgColor = if (isDark) Color(0xFF282522) else Color(0xFFEBE5DA)

    var searchQuery by remember { mutableStateOf("") }
    var activeCategoryFilter by remember { mutableStateOf(initialCategoryFilter) }

    val filteredExpenses = expenses.filter { expense ->
        val matchesSearch = searchQuery.isBlank() || expense.title.contains(searchQuery, ignoreCase = true) || expense.category.contains(searchQuery, ignoreCase = true)
        val matchesCategory = activeCategoryFilter.isNullOrBlank() || expense.category.equals(activeCategoryFilter, ignoreCase = true)
        matchesSearch && matchesCategory
    }

    LazyColumn(
        modifier = modifier.fillMaxSize().padding(horizontal = 20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Spacer(Modifier.height(8.dp))
            Column {
                Text("Movimenti", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                Text("Tutte le tue uscite", color = subTextColor, fontSize = 14.sp)
            }

            Spacer(Modifier.height(12.dp))

            if (availableMonths.size > 1) {
                MonthSelectorStrip(availableMonths, selectedMonth, isDark, onMonthSelect)
                Spacer(Modifier.height(10.dp))
            }

            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                placeholder = { Text("Cerca tra le spese...", color = subTextColor) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = subTextColor) },
                singleLine = true,
                shape = CircleShape,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Terracotta,
                    unfocusedBorderColor = softBgColor,
                    focusedContainerColor = cardBg,
                    unfocusedContainerColor = cardBg,
                    focusedTextColor = textColor,
                    unfocusedTextColor = textColor
                ),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(Modifier.height(10.dp))

            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(horizontal = 2.dp)
            ) {
                item {
                    val isAllSelected = activeCategoryFilter.isNullOrBlank()
                    Surface(
                        color = if (isAllSelected) Terracotta else cardBg,
                        shape = CircleShape,
                        shadowElevation = if (isAllSelected) 4.dp else 1.dp,
                        modifier = Modifier.clip(CircleShape).clickable {
                            activeCategoryFilter = null
                            onClearCategoryFilter()
                        }
                    ) {
                        Text(
                            "Tutte le categorie",
                            color = if (isAllSelected) Color.White else textColor,
                            fontWeight = if (isAllSelected) FontWeight.Bold else FontWeight.Medium,
                            fontSize = 12.sp,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                        )
                    }
                }

                items(allCategories) { category ->
                    val isSelected = activeCategoryFilter?.equals(category, ignoreCase = true) == true
                    val meta = getCategoryMeta(category)

                    Surface(
                        color = if (isSelected) meta.color else cardBg,
                        shape = CircleShape,
                        shadowElevation = if (isSelected) 4.dp else 1.dp,
                        modifier = Modifier.clip(CircleShape).clickable {
                            activeCategoryFilter = if (isSelected) null else category
                        }
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(16.dp)
                                    .background(if (isSelected) Color.White.copy(alpha = 0.3f) else meta.color.copy(alpha = 0.2f), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    meta.icon,
                                    contentDescription = null,
                                    tint = if (isSelected) Color.White else meta.color,
                                    modifier = Modifier.size(10.dp)
                                )
                            }
                            Spacer(Modifier.width(6.dp))
                            Text(
                                category,
                                color = if (isSelected) Color.White else textColor,
                                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                                fontSize = 12.sp
                            )
                        }
                    }
                }
            }
            Spacer(Modifier.height(4.dp))
        }

        if (filteredExpenses.isEmpty()) {
            item {
                Box(
                    modifier = Modifier.fillMaxWidth().padding(top = 40.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier.size(72.dp).background(softBgColor, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.ReceiptLong, contentDescription = null, tint = subTextColor, modifier = Modifier.size(36.dp))
                        }
                        Spacer(Modifier.height(12.dp))
                        Text("Nessuna spesa trovata", color = textColor, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        Text("Prova a modificare la ricerca o il filtro", color = subTextColor, fontSize = 13.sp)
                    }
                }
            }
        } else {
            items(filteredExpenses) { ExpenseRow(it, isDark, isPrivacyMode, onDeleteExpense) }
        }

        item { Spacer(Modifier.height(88.dp)) }
    }
}

@Composable
private fun ExpenseRow(expense: Expense, isDark: Boolean, isPrivacyMode: Boolean, onDelete: (Expense) -> Unit) {
    val meta = getCategoryMeta(expense.category)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)

    Surface(
        color = cardBg,
        shape = RoundedCornerShape(22.dp),
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(46.dp).background(meta.color.copy(alpha = 0.12f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier.size(34.dp).background(meta.color, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(meta.icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                }
            }

            Column(
                modifier = Modifier.weight(1f).padding(start = 14.dp, end = 8.dp)
            ) {
                Text(
                    text = expense.title,
                    color = textColor,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 15.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(Modifier.height(3.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        color = meta.color.copy(alpha = 0.12f),
                        shape = CircleShape,
                        modifier = Modifier.weight(1f, fill = false)
                    ) {
                        Text(
                            text = expense.category,
                            color = meta.color,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                    if (expense.month.isNotBlank()) {
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "• ${expense.month}",
                            color = Sage,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }

            Text(
                text = formatAmount(expense.amount, isPrivacyMode),
                color = textColor,
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                maxLines = 1
            )

            Spacer(Modifier.width(8.dp))

            IconButton(
                onClick = { onDelete(expense) },
                modifier = Modifier
                    .size(32.dp)
                    .background(Terracotta.copy(alpha = 0.12f), CircleShape)
            ) {
                Icon(
                    imageVector = Icons.Default.DeleteOutline,
                    contentDescription = "Elimina spesa",
                    tint = Terracotta,
                    modifier = Modifier.size(16.dp)
                )
            }
        }
    }
}

@Composable
private fun Reports(
    allExpenses: List<Expense>,
    filteredExpenses: List<Expense>,
    total: Double,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onMonthSelect: (String?) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val softBgColor = if (isDark) Color(0xFF282522) else Color(0xFFEBE5DA)

    val grouped = filteredExpenses.groupBy { it.category }
        .mapValues { it.value.sumOf(Expense::amount) }
        .toList()
        .sortedByDescending { it.second }

    val monthlyAvg = if (numMonths > 0) total / numMonths else 0.0
    val dailyAvg = if (numMonths > 0) total / (numMonths * 30.0) else 0.0
    val maxExpense = filteredExpenses.maxOfOrNull { it.amount } ?: 0.0

    // Statistiche per Anno calcolate su ALL EXPENSES così non scompaiono quando si seleziona un mese!
    val yearlyGrouped = remember(allExpenses) {
        allExpenses.groupBy { extractYear(it.month) }
            .mapValues { entry ->
                val yearExpenses = entry.value
                val yearTotal = yearExpenses.sumOf { it.amount }
                val yearMonths = yearExpenses.map { it.month }.distinct().size.coerceAtLeast(1)
                val yearMonthlyAvg = yearTotal / yearMonths
                Triple(yearTotal, yearMonths, yearMonthlyAvg)
            }
            .toList()
            .sortedByDescending { it.first }
    }

    var selectedCategoryFilter by remember { mutableStateOf<String?>(null) }

    LazyColumn(
        modifier = modifier.fillMaxSize().padding(horizontal = 20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Spacer(Modifier.height(8.dp))
            Text("Report & Statistiche", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            Text("Analisi dettagliata e KPI della tua spesa", color = subTextColor, fontSize = 14.sp)
        }

        if (availableMonths.size > 1) {
            item {
                MonthSelectorStrip(availableMonths, selectedMonth, isDark, onMonthSelect)
            }
        }

        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                // Media Mensile
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(24.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.weight(1f)
                ) {
                    Column(Modifier.padding(14.dp), horizontalAlignment = Alignment.Start) {
                        Box(
                            modifier = Modifier.size(32.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.CalendarMonth, contentDescription = null, tint = Terracotta, modifier = Modifier.size(16.dp))
                        }
                        Spacer(Modifier.height(8.dp))
                        Text(if (numMonths > 1) "Media / Mese" else "Totale Mese", color = subTextColor, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                        Text(formatAmount(monthlyAvg, isPrivacyMode), color = textColor, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                    }
                }

                // Media Giornaliera
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(24.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.weight(1f)
                ) {
                    Column(Modifier.padding(14.dp), horizontalAlignment = Alignment.Start) {
                        Box(
                            modifier = Modifier.size(32.dp).background(Sage.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.TrendingUp, contentDescription = null, tint = Sage, modifier = Modifier.size(16.dp))
                        }
                        Spacer(Modifier.height(8.dp))
                        Text("Media / Giorno", color = subTextColor, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                        Text(formatAmount(dailyAvg, isPrivacyMode), color = textColor, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                    }
                }

                // Spesa Max
                Surface(
                    color = cardBg,
                    shape = RoundedCornerShape(24.dp),
                    shadowElevation = 2.dp,
                    modifier = Modifier.weight(1f)
                ) {
                    Column(Modifier.padding(14.dp), horizontalAlignment = Alignment.Start) {
                        Box(
                            modifier = Modifier.size(32.dp).background(Ochre.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.PieChart, contentDescription = null, tint = Ochre, modifier = Modifier.size(16.dp))
                        }
                        Spacer(Modifier.height(8.dp))
                        Text("Spesa Max", color = subTextColor, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                        Text(formatAmount(maxExpense, isPrivacyMode), color = textColor, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        // STATISTICHE PER ANNO
        if (yearlyGrouped.isNotEmpty()) {
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = cardBg),
                    shape = RoundedCornerShape(32.dp),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier.size(32.dp).background(Terracotta.copy(alpha = 0.15f), CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.CalendarMonth, contentDescription = null, tint = Terracotta, modifier = Modifier.size(16.dp))
                                }
                                Spacer(Modifier.width(10.dp))
                                Text("Andamento per Anno", color = textColor, fontWeight = FontWeight.Bold, fontSize = 17.sp)
                            }
                            Surface(
                                color = softBgColor,
                                shape = CircleShape
                            ) {
                                Text(
                                    "${yearlyGrouped.size} ${if (yearlyGrouped.size == 1) "anno" else "anni"}",
                                    color = Terracotta,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                )
                            }
                        }

                        Spacer(Modifier.height(16.dp))

                        yearlyGrouped.forEach { (year, stats) ->
                            val (yearTotal, yearMonths, yearMonthlyAvg) = stats

                            Surface(
                                color = softBgColor.copy(alpha = 0.5f),
                                shape = RoundedCornerShape(20.dp),
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)
                            ) {
                                Column(Modifier.padding(14.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Surface(
                                                color = Terracotta,
                                                shape = CircleShape
                                            ) {
                                                Text(
                                                    year,
                                                    color = Color.White,
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                                )
                                            }
                                            Spacer(Modifier.width(10.dp))
                                            Text(
                                                "$yearMonths mesi registrati",
                                                color = subTextColor,
                                                fontSize = 12.sp,
                                                fontWeight = FontWeight.Medium
                                            )
                                        }

                                        Text(
                                            formatAmount(yearTotal, isPrivacyMode),
                                            color = textColor,
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 16.sp
                                        )
                                    }

                                    Spacer(Modifier.height(8.dp))

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            "Media mensile $year:",
                                            color = subTextColor,
                                            fontSize = 12.sp
                                        )
                                        Text(
                                            "${formatAmount(yearMonthlyAvg, isPrivacyMode)} / mese",
                                            color = Sage,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 13.sp
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = cardBg),
                shape = RoundedCornerShape(32.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Distribuzione Spese", color = textColor, fontWeight = FontWeight.Bold, fontSize = 17.sp)
                        if (selectedCategoryFilter != null) {
                            Surface(
                                color = softBgColor,
                                shape = CircleShape,
                                modifier = Modifier.clip(CircleShape).clickable { selectedCategoryFilter = null }
                            ) {
                                Text(
                                    "Mostra tutti",
                                    color = Terracotta,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                )
                            }
                        }
                    }

                    Spacer(Modifier.height(16.dp))

                    CircularDonutChart(
                        groupedExpenses = grouped,
                        total = total,
                        isDark = isDark,
                        isPrivacyMode = isPrivacyMode,
                        selectedCategory = selectedCategoryFilter,
                        onSelectCategory = { selectedCategoryFilter = it }
                    )

                    Spacer(Modifier.height(20.dp))

                    grouped.forEach { (category, amount) ->
                        val meta = getCategoryMeta(category)
                        val percentage = if (total > 0) ((amount / total) * 100).toInt() else 0
                        val isSelected = selectedCategoryFilter == category

                        Surface(
                            color = if (isSelected) meta.color.copy(alpha = 0.08f) else Color.Transparent,
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                                .clickable {
                                    selectedCategoryFilter = if (isSelected) null else category
                                }
                                .padding(vertical = 4.dp)
                        ) {
                            Column(Modifier.padding(horizontal = 8.dp, vertical = 8.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Box(
                                        modifier = Modifier.size(32.dp).background(meta.color, CircleShape),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(meta.icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                                    }
                                    Spacer(Modifier.width(10.dp))
                                    Text(
                                        category,
                                        color = textColor,
                                        fontWeight = FontWeight.SemiBold,
                                        fontSize = 14.sp,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis,
                                        modifier = Modifier.weight(1f, fill = false)
                                    )

                                    Spacer(Modifier.width(8.dp))

                                    Surface(
                                        color = meta.color.copy(alpha = 0.15f),
                                        shape = CircleShape
                                    ) {
                                        Text(
                                            if (isPrivacyMode) "••%" else "$percentage%",
                                            color = meta.color,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 11.sp,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                                        )
                                    }
                                    Spacer(Modifier.width(8.dp))
                                    Text(formatAmount(amount, isPrivacyMode), color = textColor, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                }

                                Spacer(Modifier.height(6.dp))

                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(8.dp)
                                        .background(softBgColor, CircleShape)
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth((percentage / 100f).coerceIn(0.02f, 1f))
                                            .height(8.dp)
                                            .background(meta.color, CircleShape)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

        item { Spacer(Modifier.height(88.dp)) }
    }
}

@Composable
private fun CircularDonutChart(
    groupedExpenses: List<Pair<String, Double>>,
    total: Double,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    selectedCategory: String?,
    onSelectCategory: (String?) -> Unit,
    modifier: Modifier = Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val softBgColor = if (isDark) Color(0xFF282522) else Color(0xFFEBE5DA)

    var animProgress by remember { mutableStateOf(0f) }
    val progressAnimation by animateFloatAsState(
        targetValue = animProgress,
        animationSpec = tween(durationMillis = 1000, easing = FastOutSlowInEasing),
        label = "donutAnimation"
    )

    LaunchedEffect(Unit) {
        animProgress = 1f
    }

    Box(
        modifier = modifier.size(230.dp),
        contentAlignment = Alignment.Center
    ) {
        Canvas(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp)
                .clickable { onSelectCategory(null) }
        ) {
            val strokeWidth = 28.dp.toPx()
            val diameter = size.minDimension - strokeWidth
            val topLeft = Offset((size.width - diameter) / 2, (size.height - diameter) / 2)
            val arcSize = Size(diameter, diameter)

            drawArc(
                color = softBgColor,
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = strokeWidth)
            )

            if (total > 0) {
                var currentStartAngle = -90f
                val gapDegree = if (groupedExpenses.size > 1) 4f else 0f

                groupedExpenses.forEach { (category, amount) ->
                    val sweepAngle = ((amount / total).toFloat() * 360f - gapDegree) * progressAnimation
                    val meta = getCategoryMeta(category)
                    val isSelected = selectedCategory == category

                    if (sweepAngle > 0f) {
                        drawArc(
                            color = if (selectedCategory == null || isSelected) meta.color else meta.color.copy(alpha = 0.25f),
                            startAngle = currentStartAngle,
                            sweepAngle = sweepAngle.coerceAtLeast(1f),
                            useCenter = false,
                            topLeft = topLeft,
                            size = arcSize,
                            style = Stroke(
                                width = if (isSelected) strokeWidth * 1.3f else strokeWidth,
                                cap = StrokeCap.Round
                            )
                        )
                    }
                    currentStartAngle += (amount / total).toFloat() * 360f * progressAnimation
                }
            }
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.padding(horizontal = 24.dp)
        ) {
            val displayCategory = selectedCategory
            val displayAmount = if (displayCategory != null) {
                groupedExpenses.firstOrNull { it.first == displayCategory }?.second ?: total
            } else {
                total
            }

            Box(
                modifier = Modifier
                    .size(42.dp)
                    .background(
                        if (displayCategory != null) getCategoryMeta(displayCategory).color.copy(alpha = 0.15f) else Terracotta.copy(alpha = 0.12f),
                        CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (displayCategory != null) getCategoryMeta(displayCategory).icon else Icons.Default.PieChart,
                    contentDescription = null,
                    tint = if (displayCategory != null) getCategoryMeta(displayCategory).color else Terracotta,
                    modifier = Modifier.size(22.dp)
                )
            }
            Spacer(Modifier.height(4.dp))
            Text(
                text = displayCategory ?: "Totale Mese",
                color = subTextColor,
                fontSize = 12.sp,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = formatAmount(displayAmount, isPrivacyMode),
                color = textColor,
                fontSize = 20.sp,
                fontWeight = FontWeight.ExtraBold
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale

    // IA State
    var aiInputText by remember { mutableStateOf("") }
    val parsedAi = remember(aiInputText) { AiExpenseParser.parseText(aiInputText) }

    // Manual State
    var manualTitle by remember { mutableStateOf("") }
    var manualAmount by remember { mutableStateOf("") }
    var manualCategory by remember { mutableStateOf(allCategories[0]) }
    var dropdownExpanded by remember { mutableStateOf(false) }

    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(32.dp),
        containerColor = dialogBg,
        title = {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            if (selectedTabMode == 0) Icons.Default.AutoAwesome else Icons.Default.Add,
                            contentDescription = null,
                            tint = Terracotta
                        )
                    }
                    Spacer(Modifier.width(12.dp))
                    Text("Nuova Spesa", color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                }

                Spacer(Modifier.height(16.dp))

                TabRow(
                    selectedTabIndex = selectedTabMode,
                    containerColor = Color.Transparent,
                    contentColor = Terracotta,
                    indicator = { tabPositions ->
                        if (selectedTabMode < tabPositions.size) {
                            TabRowDefaults.SecondaryIndicator(
                                Modifier.tabIndicatorOffset(tabPositions[selectedTabMode]),
                                color = Terracotta,
                                height = 3.dp
                            )
                        }
                    }
                ) {
                    Tab(
                        selected = selectedTabMode == 0,
                        onClick = { selectedTabMode = 0 },
                        text = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.AutoAwesome, contentDescription = null, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Inserimento IA", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            }
                        }
                    )
                    Tab(
                        selected = selectedTabMode == 1,
                        onClick = { selectedTabMode = 1 },
                        text = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Edit, contentDescription = null, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Manuale", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            }
                        }
                    )
                }
            }
        },
        text = {
            if (selectedTabMode == 0) {
                // INSERIMENTO IA
                Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    Text(
                        "Scrivi o incolla la spesa in testo libero (es. 'Pranzo di lavoro 18.50 euro al ristorante'):",
                        color = textColor.copy(alpha = 0.8f),
                        fontSize = 13.sp,
                        lineHeight = 18.sp
                    )

                    OutlinedTextField(
                        value = aiInputText,
                        onValueChange = { aiInputText = it },
                        placeholder = { Text("es. Spesa supermercato 35.40€", color = Sage) },
                        minLines = 3,
                        maxLines = 4,
                        shape = RoundedCornerShape(20.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    // Prompt Esempi Rapidi
                    Text("Suggerimenti rapidi:", color = textColor, fontWeight = FontWeight.SemiBold, fontSize = 12.sp)
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(
                            "Caffè e cornetto 3,50€",
                            "Spesa Conad 42,80€",
                            "Bolletta luce 75€ casa",
                            "Rifornimento benzina 50 euro"
                        ).forEach { sample ->
                            item {
                                Surface(
                                    color = Terracotta.copy(alpha = 0.12f),
                                    shape = CircleShape,
                                    modifier = Modifier.clip(CircleShape).clickable { aiInputText = sample }
                                ) {
                                    Text(
                                        sample,
                                        color = Terracotta,
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                    )
                                }
                            }
                        }
                    }

                    // Anteprima IA
                    if (aiInputText.isNotBlank()) {
                        Surface(
                            color = Terracotta.copy(alpha = 0.08f),
                            shape = RoundedCornerShape(20.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Column(Modifier.padding(14.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = Terracotta, modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text("Anteprima IA", color = Terracotta, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                                }
                                Spacer(Modifier.height(8.dp))
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(Modifier.weight(1f)) {
                                        Text(parsedAi.title, color = textColor, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                        Spacer(Modifier.height(2.dp))
                                        val meta = getCategoryMeta(parsedAi.category)
                                        Surface(
                                            color = meta.color.copy(alpha = 0.15f),
                                            shape = CircleShape
                                        ) {
                                            Text(
                                                parsedAi.category,
                                                color = meta.color,
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold,
                                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                                            )
                                        }
                                    }

                                    Text(
                                        if (parsedAi.amount != null) NumberFormat.getCurrencyInstance(Locale.ITALY).format(parsedAi.amount) else "Importo mancante",
                                        color = if (parsedAi.amount != null) Sage else Terracotta,
                                        fontWeight = FontWeight.ExtraBold,
                                        fontSize = 15.sp
                                    )
                                }
                            }
                        }
                    }
                }
            } else {
                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    OutlinedTextField(
                        value = manualTitle,
                        onValueChange = { manualTitle = it },
                        label = { Text("Descrizione") },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    OutlinedTextField(
                        value = manualAmount,
                        onValueChange = { manualAmount = it },
                        label = { Text("Importo (€)") },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    Text("Categoria", color = textColor, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)

                    ExposedDropdownMenuBox(
                        expanded = dropdownExpanded,
                        onExpandedChange = { dropdownExpanded = !dropdownExpanded },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        val currentMeta = getCategoryMeta(manualCategory)
                        OutlinedTextField(
                            value = manualCategory,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Seleziona categoria") },
                            leadingIcon = {
                                Box(
                                    modifier = Modifier
                                        .size(28.dp)
                                        .background(currentMeta.color.copy(alpha = 0.15f), CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = currentMeta.icon,
                                        contentDescription = null,
                                        tint = currentMeta.color,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = dropdownExpanded) },
                            shape = RoundedCornerShape(16.dp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Terracotta,
                                focusedLabelColor = Terracotta,
                                focusedTextColor = textColor,
                                unfocusedTextColor = textColor
                            ),
                            modifier = Modifier
                                .menuAnchor(MenuAnchorType.PrimaryNotEditable, true)
                                .fillMaxWidth()
                        )

                        ExposedDropdownMenu(
                            expanded = dropdownExpanded,
                            onDismissRequest = { dropdownExpanded = false },
                            modifier = Modifier.background(dialogBg)
                        ) {
                            allCategories.forEach { category ->
                                val meta = getCategoryMeta(category)
                                DropdownMenuItem(
                                    text = {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Box(
                                                modifier = Modifier
                                                    .size(28.dp)
                                                    .background(meta.color.copy(alpha = 0.15f), CircleShape),
                                                contentAlignment = Alignment.Center
                                            ) {
                                                Icon(
                                                    imageVector = meta.icon,
                                                    contentDescription = null,
                                                    tint = meta.color,
                                                    modifier = Modifier.size(16.dp)
                                                )
                                            }
                                            Spacer(Modifier.width(12.dp))
                                            Text(
                                                category,
                                                color = textColor,
                                                fontWeight = if (category == manualCategory) FontWeight.Bold else FontWeight.Normal
                                            )
                                        }
                                    },
                                    onClick = {
                                        manualCategory = category
                                        dropdownExpanded = false
                                    }
                                )
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    if (selectedTabMode == 0) {
                        val amount = parsedAi.amount
                        if (amount != null && amount > 0) {
                            onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth))
                        }
                    } else {
                        val parsedAmount = parseAmount(manualAmount)
                        if (parsedAmount != null && parsedAmount > 0) {
                            onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth))
                        }
                    }
                },
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = Terracotta)
            ) {
                Text(
                    if (selectedTabMode == 0) "Aggiungi con IA" else "Aggiungi",
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 8.dp)
                )
            }
        },
        dismissButton = {
            TextButton(
                onClick = onDismiss,
                shape = CircleShape
            ) {
                Text("Annulla", color = Sage)
            }
        }
    )
}

@Composable
private fun SetBudgetDialog(
    currentBudget: Double?,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onSave: (Double?) -> Unit
) {
    var budgetText by remember { mutableStateOf(currentBudget?.toString() ?: "") }
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(32.dp),
        containerColor = dialogBg,
        title = {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .background(Sage.copy(alpha = 0.15f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Sage)
                }
                Spacer(Modifier.width(12.dp))
                Text("Budget Mensile", color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
            }
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(
                    "Imposta il tetto di spesa desiderato per ciascun mese. L'anello di progresso si aggiornerà automaticamente.",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 13.sp
                )
                OutlinedTextField(
                    value = budgetText,
                    onValueChange = { budgetText = it },
                    label = { Text("Budget Mensile (€)") },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Sage,
                        focusedLabelColor = Sage,
                        focusedTextColor = textColor,
                        unfocusedTextColor = textColor
                    ),
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val parsed = parseAmount(budgetText)
                    onSave(parsed)
                },
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = Sage)
            ) {
                Text("Salva", fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 8.dp))
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss, shape = CircleShape) {
                Text("Annulla", color = Terracotta)
            }
        }
    )
}

/**
 * Utility per l'importazione di fogli spesa da file .xlsx (Excel OpenXML) e .csv.
 * Estrae rigorosamente la Tabella Principale (Colonne A-F, Righe 3-39) ignorando i riepiloghi.
 */
object XlsSheetImporter {

    internal fun parseXlsxBytesForTest(bytes: ByteArray): List<Expense> =
        parseXlsxStream(ByteArrayInputStream(bytes))

    internal fun parseCsvContentForTest(content: String): List<Expense> =
        parseCsvStream(content.byteInputStream())

    internal fun parseFileBytesForTest(fileName: String, bytes: ByteArray): List<Expense> =
        parseFileBytes(fileName, bytes)

    fun importFromUri(context: Context, uri: Uri): List<Expense> {
        val fileName = getFileName(context, uri).lowercase()

        return try {
            context.contentResolver.openInputStream(uri)?.use { parseFileBytes(fileName, it.readBytes()) } ?: emptyList()
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    private fun parseFileBytes(fileName: String, bytes: ByteArray): List<Expense> {
        if (bytes.isEmpty()) return emptyList()
        if (fileName.endsWith(".xls") && !fileName.endsWith(".xlsx")) return emptyList()

        val isOpenXml = bytes.size >= 2 && bytes[0] == 'P'.code.toByte() && bytes[1] == 'K'.code.toByte()
        return if (fileName.endsWith(".xlsx") || fileName.endsWith(".xlsm") || isOpenXml) {
            parseXlsxStream(bytes.inputStream())
        } else {
            parseCsvStream(bytes.inputStream())
        }
    }

    private fun getFileName(context: Context, uri: Uri): String {
        var name = "file"
        val cursor = context.contentResolver.query(uri, null, null, null, null)
        cursor?.use {
            if (it.moveToFirst()) {
                val index = it.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (index != -1) name = it.getString(index) ?: "file"
            }
        }
        return name
    }

    private fun parseCsvStream(inputStream: InputStream): List<Expense> {
        val lines = inputStream.bufferedReader(Charsets.UTF_8).useLines { sequence -> 
            sequence.filter { it.isNotBlank() }.toList() 
        }
        if (lines.isEmpty()) return emptyList()

        val delimiter = detectDelimiter(lines)
        val records = lines.map { parseCsvLine(it, delimiter) }.filter { it.any(String::isNotBlank) }
        if (records.isEmpty()) return emptyList()

        val expenses = mutableListOf<Expense>()

        // 1. App Backup Format (Mese, Descrizione, Categoria, Importo)
        val header = records.first().map { it.trim().removePrefix("\uFEFF").lowercase(Locale.ITALY) }
        var monthCol = -1
        var titleCol = -1
        var categoryCol = -1
        var amountCol = -1

        header.forEachIndexed { idx, colName ->
            if (colName.contains("mese") || colName.contains("data") || colName.contains("periodo")) monthCol = idx
            else if (colName.contains("descriz") || colName.contains("causale") || colName.contains("nota") || colName.contains("titolo")) titleCol = idx
            else if (colName.contains("categor")) categoryCol = idx
            else if (colName.contains("importo") || colName.contains("spesa") || colName.contains("totale") || colName.contains("valore") || colName.contains("euro")) amountCol = idx
        }

        if (amountCol != -1) {
            for (record in records.drop(1)) {
                if (record.isEmpty() || record.all { it.isBlank() }) continue
                
                var amount: Double? = null
                if (amountCol < record.size) {
                    amount = parseAmount(record[amountCol])
                }

                if (amount == null || amount <= 0) {
                    for (cell in record) {
                        val candidate = parseAmount(cell)
                        if (candidate != null && candidate > 0) {
                            amount = candidate
                            break
                        }
                    }
                }

                if (amount != null && amount > 0) {
                    var title = if (titleCol != -1 && titleCol < record.size) record[titleCol].trim() else ""
                    if (title.isBlank()) {
                        title = record.firstOrNull { parseAmount(it) == null && it.length > 2 }?.trim() ?: "Spesa"
                    }
                    
                    var category = if (categoryCol != -1 && categoryCol < record.size) record[categoryCol].trim() else ""
                    if (category.isBlank()) {
                        category = "Altro"
                    }

                    var month = if (monthCol != -1 && monthCol < record.size) record[monthCol].trim() else "settembre 26"
                    if (month.isBlank()) month = "settembre 26"

                    expenses.add(Expense(title = title.ifBlank { "Spesa" }, category = category.ifBlank { "Altro" }, amount = amount, month = month))
                }
            }
            if (expenses.isNotEmpty()) return expenses
        }

        // 2. Formato Intermedio FM (se le righe hanno il separatore interno '|')
        val isIntermediateFm = records.any { parts ->
            parts.size >= 3 && parts[1].trim().toIntOrNull() != null && parts[2].contains("|")
        }

        if (isIntermediateFm) {
            val categoryHeaderMap = mutableMapOf<Int, String>()
            for (parts in records) {
                if (parts.size < 3) continue

                val sheetName = parts[0].trim().ifBlank { "settembre 26" }
                val rowNum = parts[1].trim().toIntOrNull() ?: continue
                val values = parts[2].split("|").map { it.trim() }

                if (rowNum == 2) {
                    categoryHeaderMap.clear()
                    values.take(6).forEachIndexed { colIndex, colName ->
                        if (colName.isNotBlank() && !colName.uppercase(Locale.ITALY).startsWith("TOTALE")) {
                            categoryHeaderMap[colIndex] = mapColumnToCategory(colName)
                        }
                    }
                } else if (rowNum in 3..39) {
                    val note = if (values.size > 7) values[7] else ""
                    values.take(6).forEachIndexed { colIndex, valStr ->
                        val category = categoryHeaderMap[colIndex]
                        val amount = parseAmount(valStr)
                        if (category != null && amount != null && amount > 0) {
                            val title = if (colIndex == 5 && note.isNotBlank()) note else category
                            expenses.add(Expense(title = title, category = category, amount = amount, month = sheetName))
                        }
                    }
                }
            }
            if (expenses.isNotEmpty()) return expenses
        }

        // 3. Formato Generico Sconosciuto (fallback: analizziamo riga per riga per trovare l'importo e la stringa descrittiva)
        val dataRows = if (amountCol != -1 || titleCol != -1) records.drop(1) else records
        for (record in dataRows) {
            if (record.isEmpty() || record.all { it.isBlank() }) continue

            var amount: Double? = null
            var title = ""
            for (cell in record) {
                val candidate = parseAmount(cell)
                if (candidate != null && candidate > 0 && amount == null) {
                    amount = candidate
                } else if (parseAmount(cell) == null && cell.length > 2 && title.isBlank()) {
                    title = cell.trim()
                }
            }

            if (amount != null && amount > 0) {
                val parsedAi = AiExpenseParser.parseText(title)
                expenses.add(
                    Expense(
                        title = parsedAi.title.ifBlank { title.ifBlank { "Spesa" } },
                        category = parsedAi.category,
                        amount = amount,
                        month = "settembre 26"
                    )
                )
            }
        }

        return expenses
    }

    private fun detectDelimiter(lines: List<String>): Char {
        var comma = 0
        var semicolon = 0
        var tab = 0
        for (line in lines.take(5)) {
            var inQuotes = false
            for (c in line) {
                if (c == '"') inQuotes = !inQuotes
                if (!inQuotes) {
                    when (c) {
                        ',' -> comma++
                        ';' -> semicolon++
                        '\t' -> tab++
                    }
                }
            }
        }
        return when {
            semicolon > comma && semicolon > tab -> ';'
            tab > comma && tab > semicolon -> '\t'
            else -> ','
        }
    }

    private fun parseCsvLine(line: String, delimiter: Char = ','): List<String> {
        val fields = mutableListOf<String>()
        val field = StringBuilder()
        var quoted = false
        var index = 0

        while (index < line.length) {
            val character = line[index]
            when {
                character == '"' && quoted && index + 1 < line.length && line[index + 1] == '"' -> {
                    field.append('"')
                    index++
                }
                character == '"' -> quoted = !quoted
                character == delimiter && !quoted -> {
                    fields.add(field.toString().trim())
                    field.clear()
                }
                else -> field.append(character)
            }
            index++
        }
        fields.add(field.toString().trim().trimEnd('\r'))
        return fields
    }

    private fun parseXlsxStream(inputStream: InputStream): List<Expense> {
        val expenses = mutableListOf<Expense>()
        val zipStream = ZipInputStream(inputStream)

        val sharedStrings = mutableListOf<String>()
        val sheetDataMap = mutableMapOf<String, ByteArray>()
        var workbookXmlBytes: ByteArray? = null
        var workbookRelsBytes: ByteArray? = null

        var entry = zipStream.nextEntry
        while (entry != null) {
            val entryName = entry.name.replace("\\", "/")
            when {
                entryName == "xl/sharedStrings.xml" -> {
                    sharedStrings.addAll(parseSharedStrings(zipStream.readBytes()))
                }
                entryName == "xl/workbook.xml" -> {
                    workbookXmlBytes = zipStream.readBytes()
                }
                entryName == "xl/_rels/workbook.xml.rels" -> {
                    workbookRelsBytes = zipStream.readBytes()
                }
                entryName.startsWith("xl/worksheets/") && entryName.endsWith(".xml") -> {
                    sheetDataMap[entryName] = zipStream.readBytes()
                }
            }
            zipStream.closeEntry()
            entry = zipStream.nextEntry
        }

        val relsMap = if (workbookRelsBytes != null) parseWorkbookRels(workbookRelsBytes) else emptyMap()
        val sheetsList = if (workbookXmlBytes != null) parseWorkbookSheets(workbookXmlBytes) else emptyList()

        if (sheetsList.isNotEmpty()) {
            sheetsList.forEach { (sheetName, rId) ->
                val normalizedSheetName = sheetName.trim().uppercase(Locale.ITALY)
                if (normalizedSheetName == "TEMPLATE" || normalizedSheetName.contains("RIEPILOGO") || normalizedSheetName.contains("SOMMARIO")) {
                    return@forEach
                }

                val targetPath = relsMap[rId] ?: ""
                val fullPath = normalizeZipPath(targetPath)
                val sheetBytes = sheetDataMap[fullPath]
                    ?: sheetDataMap.entries.firstOrNull { it.key.endsWith(targetPath.trimStart('/')) }?.value

                if (sheetBytes != null) {
                    expenses.addAll(parseSheetXml(sheetBytes, sheetName, sharedStrings))
                }
            }
        } else {
            sheetDataMap.entries.forEachIndexed { index, (_, bytes) ->
                expenses.addAll(parseSheetXml(bytes, "Mese ${index + 1}", sharedStrings))
            }
        }

        return expenses
    }

    private fun parseWorkbookRels(bytes: ByteArray): Map<String, String> {
        val map = mutableMapOf<String, String>()
        val parser = xmlParser(bytes)

        var eventType = parser.eventType
        while (eventType != XmlPullParser.END_DOCUMENT) {
            if (eventType == XmlPullParser.START_TAG && parser.name == "Relationship") {
                val id = parser.getAttributeValue(null, "Id")
                val target = parser.getAttributeValue(null, "Target")
                if (id != null && target != null) {
                    map[id] = target
                }
            }
            eventType = parser.next()
        }
        return map
    }

    private fun normalizeZipPath(target: String): String {
        val parts = target.trimStart('/').split('/')
        val normalized = ArrayDeque<String>()
        parts.forEach { part ->
            when (part) {
                "", "." -> Unit
                ".." -> if (normalized.isNotEmpty()) normalized.removeLast()
                else -> normalized.addLast(part)
            }
        }
        val path = normalized.joinToString("/")
        return if (path.startsWith("xl/")) path else "xl/$path"
    }

    private fun parseWorkbookSheets(bytes: ByteArray): List<Pair<String, String>> {
        val list = mutableListOf<Pair<String, String>>()
        val parser = xmlParser(bytes)

        var eventType = parser.eventType
        while (eventType != XmlPullParser.END_DOCUMENT) {
            if (eventType == XmlPullParser.START_TAG && parser.name == "sheet") {
                val name = parser.getAttributeValue(null, "name")
                val rId = parser.getAttributeValue("http://schemas.openxmlformats.org/officeDocument/2006/relationships", "id")
                    ?: parser.getAttributeValue(null, "r:id")
                    ?: parser.getAttributeValue(null, "id")
                if (name != null && rId != null) {
                    list.add(name to rId)
                }
            }
            eventType = parser.next()
        }
        return list
    }

    private fun parseSharedStrings(bytes: ByteArray): List<String> {
        val strings = mutableListOf<String>()
        val parser = xmlParser(bytes)

        var eventType = parser.eventType
        var currentText = StringBuilder()
        var insideT = false

        while (eventType != XmlPullParser.END_DOCUMENT) {
            val name = parser.name
            when (eventType) {
                XmlPullParser.START_TAG -> {
                    if (name == "si") {
                        currentText = StringBuilder()
                    } else if (name == "t") {
                        insideT = true
                    }
                }
                XmlPullParser.TEXT -> {
                    if (insideT) currentText.append(parser.text)
                }
                XmlPullParser.END_TAG -> {
                    if (name == "t") {
                        insideT = false
                    } else if (name == "si") {
                        strings.add(currentText.toString())
                    }
                }
            }
            eventType = parser.next()
        }
        return strings
    }

    private fun parseSheetXml(bytes: ByteArray, sheetName: String, sharedStrings: List<String>): List<Expense> {
        val expenses = mutableListOf<Expense>()
        val parser = xmlParser(bytes)

        var eventType = parser.eventType
        var currentRowNum = -1
        val rowCells = mutableMapOf<Int, String>()
        val categoryHeaderMap = mutableMapOf<Int, String>()

        while (eventType != XmlPullParser.END_DOCUMENT) {
            when (eventType) {
                XmlPullParser.START_TAG -> {
                    if (parser.name == "row") {
                        currentRowNum = parser.getAttributeValue(null, "r")?.toIntOrNull() ?: -1
                        rowCells.clear()
                    } else if (parser.name == "c") {
                        val cellRef = parser.getAttributeValue(null, "r") ?: ""
                        val cellType = parser.getAttributeValue(null, "t") ?: ""
                        val colIndex = getColIndexFromRef(cellRef)

                        var cellVal = readCellValue(parser, cellType)

                        if (cellType == "s" && cellVal.toIntOrNull() != null) {
                            val strIdx = cellVal.toInt()
                            if (strIdx in sharedStrings.indices) cellVal = sharedStrings[strIdx]
                        }

                        if (colIndex != -1 && cellVal.isNotBlank()) {
                            rowCells[colIndex] = cellVal
                        }
                    }
                }
                XmlPullParser.END_TAG -> {
                    if (parser.name == "row") {
                        if (currentRowNum == 2) {
                            categoryHeaderMap.clear()
                            for (colIdx in 0..5) {
                                val valStr = rowCells[colIdx] ?: ""
                                if (valStr.isNotBlank() && !valStr.startsWith("TOTALE")) {
                                    categoryHeaderMap[colIdx] = mapColumnToCategory(valStr)
                                }
                            }
                        } else if (currentRowNum in 3..39) {
                            val note = rowCells[7] ?: ""
                            for (colIdx in 0..5) {
                                val valStr = rowCells[colIdx]
                                val category = categoryHeaderMap[colIdx]
                                val amount = parseAmount(valStr)
                                if (category != null && amount != null && amount > 0) {
                                    val title = if (colIdx == 5 && note.isNotBlank()) {
                                        note
                                    } else {
                                        category
                                    }
                                    expenses.add(Expense(title, category, amount, month = sheetName))
                                }
                            }
                        }
                    }
                }
            }
            eventType = parser.next()
        }

        return expenses
    }

    private fun xmlParser(bytes: ByteArray): XmlPullParser {
        return KXmlParser().apply {
            setInput(ByteArrayInputStream(bytes), "UTF-8")
        }
    }

    private fun readCellValue(parser: XmlPullParser, cellType: String): String {
        val value = StringBuilder()
        var captureText = false
        var eventType = parser.next()

        while (eventType != XmlPullParser.END_DOCUMENT) {
            if (eventType == XmlPullParser.END_TAG && parser.name == "c") break

            when (eventType) {
                XmlPullParser.START_TAG -> {
                    captureText = parser.name == "v" || (cellType == "inlineStr" && parser.name == "t")
                }
                XmlPullParser.TEXT -> if (captureText) value.append(parser.text)
                XmlPullParser.END_TAG -> if (parser.name == "v" || parser.name == "t") captureText = false
            }
            eventType = parser.next()
        }
        return value.toString()
    }

    private fun getColIndexFromRef(ref: String): Int {
        val colLetters = ref.takeWhile { it.isLetter() }.uppercase()
        if (colLetters.isEmpty()) return -1
        var colIndex = 0
        for (ch in colLetters) {
            colIndex = colIndex * 26 + (ch - 'A' + 1)
        }
        return colIndex - 1
    }

    private fun mapColumnToCategory(colName: String): String {
        val norm = colName.lowercase().trim()
        return when {
            norm.contains("spesa") -> "Spesa"
            norm.contains("trasport") -> "Trasporti"
            norm.contains("bar") || norm.contains("ristorant") || norm.contains("uscit") || norm.contains("locali") -> "Bar / Ristoranti / Uscite"
            norm.contains("medic") || norm.contains("salute") -> "Mediche"
            norm.contains("fitto") || norm.contains("bollett") || norm.contains("casa") -> "Fitto / Bollette / Casa"
            norm.contains("regal") -> "Regali"
            norm.contains("ricorrent") || norm.contains("abbonament") -> "Ricorrenti"
            else -> "Altro"
        }
    }
}
