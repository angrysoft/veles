/* =============================================================
   Veles Linux — Calamares Installer Slideshow
   show.qml  |  slideshowAPI: 1
   Palette synchronized with branding.desc sidebar colours
   ============================================================= */

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root

    // ── Palette — mirrors branding.desc sidebar colours ────────
    readonly property color bg:           "#19120c"   // sidebarBackground
    readonly property color surface:      "#211810"   // slightly lighter
    readonly property color accent:       "#feb877"   // sidebarTextHighlight
    readonly property color accentDim:    "#b07a3a"
    readonly property color accentSoft:   "#3d2710"
    readonly property color textPrimary:  "#ffede0"   // sidebarText
    readonly property color textMuted:    "#c4a882"
    readonly property color sepColor:     "#2e1f10"

    // ── Slide data ─────────────────────────────────────────────
    property var slides: [
        {
            icon:    "᚛",
            heading: "Witaj w Veles Linux",
            subhead: "System zrodzony z mocy i wolności",
            body:    "Instalacja potrwa kilka minut. W tym czasie możesz zapoznać się z tym, co oferuje Veles Linux — system stworzony z myślą o wydajności, prywatności i pełnej kontroli użytkownika."
        },
        {
            icon:    "⚡",
            heading: "Szybki i lekki",
            subhead: "Zasoby do Twojej dyspozycji",
            body:    "Veles Linux startuje w kilka sekund i pozostawia maksimum zasobów dla Twoich aplikacji. Zoptymalizowany pod kątem wydajności — działa sprawnie nawet na starszym sprzęcie."
        },
        {
            icon:    "🔒",
            heading: "Prywatność i bezpieczeństwo",
            subhead: "Twoje dane należą do Ciebie",
            body:    "Zero telemetrii. Zero ukrytych połączeń. Veles Linux szanuje Twoją prywatność od pierwszego uruchomienia — domyślnie bezpieczny, z pełną transparentnością każdej zmiany."
        },
        {
            icon:    "🎨",
            heading: "W pełni konfigurowalny",
            subhead: "Środowisko na Twój obraz",
            body:    "Każdy element interfejsu można dostosować. Wayland, Sway, KDE, GNOME — wybierz swoje środowisko i skonfiguruj je tak, jak chcesz. Veles Linux nie ogranicza Twojej wolności."
        },
        {
            icon:    "🛠",
            heading: "Narzędzia dla zaawansowanych",
            subhead: "Pełna kontrola nad systemem",
            body:    "Oparty na Arch Linux — rolling release, dostęp do AUR, najnowsze oprogramowanie zawsze w zasięgu ręki. pacman, pełna automatyzacja i skrypty bez żadnych przeszkód."
        },
        {
            icon:    "🌐",
            heading: "Społeczność Veles",
            subhead: "Nie jesteś sam",
            body:    "Dołącz do rosnącej społeczności użytkowników i deweloperów. Wiki, forum i wsparcie zawsze blisko. Odwiedź nas na veles.angrysoft.ovh i buduj z nami wolny system."
        }
    ]

    property int currentSlide: 0

    // ── Background ─────────────────────────────────────────────
    Rectangle {
        anchors.fill: parent
        color: root.bg

        // Warm glow — top left
        Rectangle {
            width: 480; height: 480
            x: -160; y: -160
            radius: 240
            color: "transparent"
            gradient: RadialGradient {
                centerX: 240; centerY: 240
                focalX: 240; focalY: 240
                radius: 240
                GradientStop { position: 0.0; color: "#2a1a08" }
                GradientStop { position: 1.0; color: "transparent" }
            }
            opacity: 0.8
        }

        // Warm glow — bottom right
        Rectangle {
            width: 360; height: 360
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: -80
            anchors.bottomMargin: -80
            radius: 180
            color: "transparent"
            gradient: RadialGradient {
                centerX: 180; centerY: 180
                focalX: 180; focalY: 180
                radius: 180
                GradientStop { position: 0.0; color: "#1e1005" }
                GradientStop { position: 1.0; color: "transparent" }
            }
            opacity: 0.7
        }

        // Top accent line
        Rectangle {
            width: parent.width; height: 2
            anchors.top: parent.top
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.25; color: root.accentDim }
                GradientStop { position: 0.65; color: root.accent }
                GradientStop { position: 1.0;  color: "transparent" }
            }
        }
    }

    // ── Slides ─────────────────────────────────────────────────
    Repeater {
        model: root.slides.length

        Item {
            anchors.fill: parent
            opacity: (index === root.currentSlide) ? 1.0 : 0.0
            visible: opacity > 0.01

            Behavior on opacity {
                NumberAnimation { duration: 550; easing.type: Easing.InOutQuad }
            }

            // ── Left panel ──────────────────────────────────────
            Rectangle {
                id: leftPanel
                width: 210
                anchors { left: parent.left; top: parent.top; bottom: parent.bottom }
                color: root.surface

                // Right-edge separator
                Rectangle {
                    width: 1; height: parent.height
                    anchors.right: parent.right
                    color: root.sepColor
                }

                Column {
                    anchors.centerIn: parent
                    spacing: 26

                    // Icon circle
                    Rectangle {
                        width: 86; height: 86
                        radius: 43
                        anchors.horizontalCenter: parent.horizontalCenter
                        color: root.accentSoft
                        border.color: root.accentDim
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: root.slides[index].icon
                            font.pixelSize: 34
                            color: root.accent
                        }
                    }

                    // Slide counter
                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: (index + 1) + " / " + root.slides.length
                        color: root.textMuted
                        font.pixelSize: 11
                        font.letterSpacing: 2
                    }

                    // Dot indicators
                    Row {
                        anchors.horizontalCenter: parent.horizontalCenter
                        spacing: 7

                        Repeater {
                            model: root.slides.length
                            Rectangle {
                                width:  modelIndex === root.currentSlide ? 20 : 6
                                height: 6
                                radius: 3
                                color:  modelIndex === root.currentSlide
                                        ? root.accent
                                        : root.accentDim
                                opacity: modelIndex === root.currentSlide ? 1.0 : 0.35

                                Behavior on width { NumberAnimation { duration: 300 } }
                                Behavior on color { ColorAnimation  { duration: 300 } }
                            }
                        }
                    }
                }

                // Brand lockup at bottom
                Column {
                    anchors {
                        bottom: parent.bottom
                        horizontalCenter: parent.horizontalCenter
                        bottomMargin: 26
                    }
                    spacing: 3

                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "VELES"
                        color: root.accent
                        font.pixelSize: 15
                        font.letterSpacing: 5
                        font.bold: true
                    }
                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "linux 1.0"
                        color: root.textMuted
                        font.pixelSize: 10
                        font.letterSpacing: 3
                    }
                }
            }

            // ── Right panel ─────────────────────────────────────
            Item {
                anchors {
                    left: leftPanel.right
                    right: parent.right
                    top: parent.top
                    bottom: parent.bottom
                    leftMargin: 52
                    rightMargin: 52
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width
                    spacing: 0

                    // Eyebrow
                    Text {
                        text: root.slides[index].subhead.toUpperCase()
                        color: root.accentDim
                        font.pixelSize: 10
                        font.letterSpacing: 3
                        font.bold: true
                        bottomPadding: 12
                    }

                    // Heading
                    Text {
                        text: root.slides[index].heading
                        color: root.textPrimary
                        font.pixelSize: 28
                        font.bold: true
                        wrapMode: Text.WordWrap
                        width: parent.width
                        lineHeight: 1.15
                        bottomPadding: 18
                    }

                    // Accent rule
                    Rectangle {
                        width: 44; height: 2
                        radius: 1
                        color: root.accent
                    }

                    Item { width: 1; height: 22 }

                    // Body
                    Text {
                        text: root.slides[index].body
                        color: root.textMuted
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                        width: parent.width
                        lineHeight: 1.75
                    }
                }
            }
        }
    }

    // ── Bottom progress bar ────────────────────────────────────
    Rectangle {
        anchors { bottom: parent.bottom; left: parent.left }
        height: 2
        color: root.accent
        width: 0

        NumberAnimation on width {
            id: progressAnim
            from: 0
            to:   root.width
            duration: slideTimer.interval
            running: true
        }
    }

    // ── Timer ──────────────────────────────────────────────────
    Timer {
        id: slideTimer
        interval: 6000
        running:  true
        repeat:   true
        onTriggered: {
            root.currentSlide = (root.currentSlide + 1) % root.slides.length
            progressAnim.restart()
        }
    }

    // ── slideshowAPI: 1 callbacks ──────────────────────────────
    function onActivate() {
        slideTimer.running  = true
        progressAnim.running = true
    }

    function onLeave() {
        slideTimer.running  = false
        progressAnim.running = false
    }
}
