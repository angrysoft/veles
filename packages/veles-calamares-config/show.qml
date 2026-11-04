/* =============================================================
   Veles Linux — Calamares Installer Slideshow
   show.qml  |  slideshowAPI: 1
   Palette synchronized with branding.desc sidebar colours
   ============================================================= */

import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation

    function nextSlide() {
        presentation.goToNextSlide();
    }

    Timer {
        id: advanceTimer
        interval: 1000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: nextSlide()
    }
    

    Slide {

        Image {
            id: background
            source: "welcome.png"
            width: 200; height: 200
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: background.horizontalCenter
            anchors.top: background.bottom
            text: qsTr("Thank you for choosing Veles Linux!<br/>")
            wrapMode: Text.WordWrap
            width: presentation.width
            horizontalAlignment: Text.Center
        }
    }

    // Slide {
    //     centeredText: qsTr("This is a second Slide element.")
    // }

    // Slide {
    //     centeredText: qsTr("This is a third Slide element.")
    // }

    // When this slideshow is loaded as a V1 slideshow, only
    // activatedInCalamares is set, which starts the timer (see above).
    //
    // In V2, also the onActivate() and onLeave() methods are called.
    // These example functions log a message (and re-start the slides
    // from the first).
    function onActivate() {
        console.log("QML Component (default slideshow) activated");
        presentation.currentSlide = 0;
    }

    function onLeave() {
        console.log("QML Component (default slideshow) deactivated");
    }
}