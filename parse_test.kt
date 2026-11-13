import java.util.Locale

fun main() {
    val csv = """
Mese;Descrizione;Categoria;Importo
settembre 26;"Cena, amici";"Bar / Ristoranti / Uscite";"24,50"
""".trimIndent()

    val lines = csv.lines()
    println("Delimiter: ${detectDelimiter(lines)}")
    lines.forEach { println(parseCsvLine(it, detectDelimiter(lines))) }
}

fun detectDelimiter(lines: List<String>): Char {
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

fun parseCsvLine(line: String, delimiter: Char = ','): List<String> {
    val result = mutableListOf<String>()
    val current = StringBuilder()
    var inQuotes = false
    var i = 0
    while (i < line.length) {
        val c = line[i]
        if (c == '"') {
            if (inQuotes && i + 1 < line.length && line[i + 1] == '"') {
                current.append('"')
                i++
            } else {
                inQuotes = !inQuotes
            }
        } else if (c == delimiter && !inQuotes) {
            result.add(current.toString().trim())
            current.clear()
        } else {
            current.append(c)
        }
        i++
    }
    result.add(current.toString().trim())
    return result
}
