package it.fm.spese

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ReminderAndDateTest {

    @Test
    fun testParseAmountFormatting() {
        assertEquals(12.5, parseAmount("12,50 €")!!, 0.001)
        assertEquals(1045.55, parseAmount("1.045,55 €")!!, 0.001)
        assertEquals(257.0, parseAmount("257")!!, 0.001)
    }

    @Test
    fun testExpenseDataClassDefaults() {
        val expense = Expense(title = "Caffè", category = "Bar / Ristoranti / Uscite", amount = 1.2)
        assertEquals("Caffè", expense.title)
        assertEquals("Bar / Ristoranti / Uscite", expense.category)
        assertEquals(1.2, expense.amount, 0.001)
        assertTrue(expense.month.isNotBlank())
        assertTrue(expense.date.isNotBlank())
    }
}
