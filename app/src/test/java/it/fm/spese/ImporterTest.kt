package it.fm.spese

import java.io.ByteArrayOutputStream
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ImporterTest {

    @Test
    fun importsInlineStringsAndSkipsTemplateSheet() {
        val expenses = XlsSheetImporter.parseXlsxBytesForTest(minimalWorkbook())

        assertEquals(2, expenses.size)
        assertEquals("settembre 26", expenses.first().month)
        assertEquals("Spesa", expenses.first().category)
        assertEquals(12.5, expenses.first().amount, 0.001)
        assertEquals("Trasporti", expenses[1].category)
    }

    @Test
    fun importsQuotedCsvAndAppBackupCsv() {
        val intermediate = XlsSheetImporter.parseCsvContentForTest(
            "mese,riga,valori\nsettembre 26,2,\"SPESA | TRASPORTI | TOTALE\"\nsettembre 26,3,\"12,50 | 4.5 | 16,99\""
        )
        val backup = XlsSheetImporter.parseCsvContentForTest(
            "Mese,Descrizione,Categoria,Importo\n\"settembre 26\",\"Cena, amici\",\"Bar / Ristoranti / Uscite\",\"24,50\""
        )

        assertEquals(2, intermediate.size)
        assertEquals(12.5, intermediate.first().amount, 0.001)
        assertEquals(24.5, backup.single().amount, 0.001)
        assertTrue(backup.single().title.contains("Cena, amici"))
    }

    @Test
    fun detectsCsvWhenDocumentProviderHasNoExtension() {
        val csv = "Mese,Descrizione,Categoria,Importo\nsettembre 26,Spesa,Spesa,\"12,50\""
        val expenses = XlsSheetImporter.parseFileBytesForTest("file", csv.toByteArray())

        assertEquals(1, expenses.size)
        assertEquals(12.5, expenses.single().amount, 0.001)
    }

    private fun minimalWorkbook(): ByteArray {
        val output = ByteArrayOutputStream()
        ZipOutputStream(output).use { zip ->
            zipEntry(zip, "xl/workbook.xml", """
                <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                  <sheets><sheet name="template" r:id="rId9"/><sheet name="settembre 26" r:id="rId4"/></sheets>
                </workbook>
            """.trimIndent())
            zipEntry(zip, "xl/_rels/workbook.xml.rels", """
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/month.xml"/>
                  <Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/template.xml"/>
                </Relationships>
            """.trimIndent())
            zipEntry(zip, "xl/worksheets/template.xml", "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\"><sheetData/></worksheet>")
            zipEntry(zip, "xl/worksheets/month.xml", """
                <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
                  <row r="2"><c r="A2" t="inlineStr"><is><t>SPESA</t></is></c><c r="B2" t="inlineStr"><is><t>TRASPORTI</t></is></c><c r="C2" t="inlineStr"><is><t>TOTALE</t></is></c></row>
                  <row r="3"><c r="A3"><v>12.5</v></c><c r="B3"><v>4.5</v></c></row>
                </sheetData></worksheet>
            """.trimIndent())
        }
        return output.toByteArray()
    }

    private fun zipEntry(zip: ZipOutputStream, name: String, content: String) {
        zip.putNextEntry(ZipEntry(name))
        zip.write(content.toByteArray())
        zip.closeEntry()
    }
}