with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix toast with composable inside lambda
content = content.replace("Toast.makeText(context, AppStrings.get(AppStrings.lingua_impostata_lang_displayname, LocalAppLanguage.current).replace(\"${lang.displayName}\", lang.displayName), Toast.LENGTH_SHORT).show()", "Toast.makeText(context, \"Lingua impostata\", Toast.LENGTH_SHORT).show()")

# Remove trailing braces
content = content.replace("""    }
    }
}

private fun Settings""", """    }
}

private fun Settings""")

content = content.replace("""    }
    }
}

@Composable
private fun SummaryCard""", """    }
}

@Composable
private fun SummaryCard""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

