import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add selectedExpense state
content = content.replace("var showSettings by remember { mutableStateOf(false) }", "var showSettings by remember { mutableStateOf(false) }\n    var selectedExpense by remember { mutableStateOf<Expense?>(null) }")

# Add ExpenseDetailScreen
expense_detail_code = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExpenseDetailScreen(
    expense: Expense,
    isDark: Boolean,
    onClose: () -> Unit,
    onDelete: () -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.dettagli_spesa, appLang), color = textColor, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onClose) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = if (isDark) Color(0xFF121110) else Color(0xFFFAF7F2)
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Spacer(Modifier.height(16.dp))
            
            Surface(
                color = cardBg,
                shape = RoundedCornerShape(16.dp),
                shadowElevation = 4.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    val catInfo = mapColumnToCategory(expense.category)
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .background(catInfo.color.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(catInfo.emoji, fontSize = 32.sp)
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(expense.title, color = textColor, fontSize = 24.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                    Spacer(Modifier.height(8.dp))
                    Text(
                        text = "-${String.format(Locale.getDefault(), "%.2f", expense.amount)} €",
                        color = Color(0xFFD95D39),
                        fontSize = 32.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
            }

            Surface(
                color = cardBg,
                shape = RoundedCornerShape(16.dp),
                shadowElevation = 2.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    DetailRow(AppStrings.get(AppStrings.categoria, appLang), expense.category, textColor, subTextColor)
                    DetailRow(AppStrings.get(AppStrings.data, appLang), expense.date, textColor, subTextColor)
                    if (expense.time.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.ora, appLang), expense.time, textColor, subTextColor)
                    }
                    if (expense.description.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.descrizione, appLang), expense.description, textColor, subTextColor)
                    }
                }
            }
            
            Spacer(Modifier.weight(1f))
            
            Button(
                onClick = { onDelete(); onClose() },
                modifier = Modifier.fillMaxWidth().height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD95D39)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Icon(Icons.Default.Delete, contentDescription = null, tint = Color.White)
                Spacer(Modifier.width(8.dp))
                Text(AppStrings.get(AppStrings.elimina, appLang), color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
fun DetailRow(label: String, value: String, textColor: Color, subTextColor: Color) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, color = subTextColor, fontSize = 16.sp)
        Text(value, color = textColor, fontSize = 16.sp, fontWeight = FontWeight.Medium)
    }
}
"""

if "fun ExpenseDetailScreen" not in content:
    content = content + "\n" + expense_detail_code

# Display ExpenseDetailScreen
show_detail_logic = """
            if (selectedExpense != null) {
                ExpenseDetailScreen(
                    expense = selectedExpense!!,
                    isDark = isDark,
                    onClose = { selectedExpense = null },
                    onDelete = { 
                        val e = selectedExpense!!
                        expenses = expenses.filter { it != e }
                        saveExpenses(context, expenses)
                    }
                )
            } else if (showSettings) {
"""

content = content.replace("if (showSettings) {", show_detail_logic)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

