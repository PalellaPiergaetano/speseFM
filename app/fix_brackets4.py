import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Rimuovo l'eccesso di parentesi alla fine di SpeseApp
# `SpeseApp` finisce attorno a 1018. Vediamo come ci arriviamo.
# Posso usare un parser o semplicemente git checkout.
# Poiché l'utente ha modificato i file "recently", non voglio perdere il suo stato.
# Posso cercare "    }\n    }\n}\n\nprivate fun launchBiometricPrompt("
# E cambiare in "}\n\nprivate fun launchBiometricPrompt("
# Rimuovo 2 parentesi in più (per il ModalNavigationDrawer e il CompositionLocalProvider)
# Aspetta, se rimuovo, tolgo chiusure.
# The errors "Expecting a top level declaration" mean there are TOO MANY closing braces.
content = content.replace(
"""    }
    }
}

private fun launchBiometricPrompt""",
"""}

private fun launchBiometricPrompt""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

