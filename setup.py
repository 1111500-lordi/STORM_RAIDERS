import cx_Freeze

build_exe_options = {
    "packages": [
        "pygame",
        "pyttsx3"
    ],
    "includes": [
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5"
    ],
    "include_files": [
        "bases",
        "recursos"
    ]
}

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/Icone.ico",
        target_name="StormRaiders.exe"
    )
]

cx_Freeze.setup(
    name="STORM RAIDERS",
    version="1.0",
    description="Jogo de piratas",
    options={
        "build_exe": build_exe_options
    },
    executables=executaveis
)