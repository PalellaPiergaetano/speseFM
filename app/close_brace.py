with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trovo dove finisce lo Scaffold.
# Invece di provare a chiuderlo manualmente, cerco "            }\n        }\n    }\n}\n\ndata class TutorialStep" e inserisco la parentesi graffa
# Manca una parentesi graffa di chiusura prima del `data class TutorialStep`.

content = content.replace(
"""            }
        }
    }
}

data class TutorialStep""", 
"""            }
        }
    }
    }
}

data class TutorialStep"""
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

