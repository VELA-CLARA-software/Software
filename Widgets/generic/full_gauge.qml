import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

Rectangle {
    width: 300
    height: 300
    color: "white"

    CircularGauge {
        objectName: "test_gauge"
        property real gauge_value: 180.0
        anchors.centerIn: parent
        value: gauge_value
        maximumValue: 360.0  // Largest Value
        minimumValue: 0.0       // Smallest Value
        style: CircularGaugeStyle {
            id: style
            tickmarkStepSize: 45.0 // Tick Marks

            tickmark: Rectangle {
                visible: styleData.value < 360 || styleData.value % 36 == 0
                implicitWidth: outerRadius * 0.02
                antialiasing: true
                implicitHeight: outerRadius * 0.06
                color: styleData.value >= 288 ? "#000000" : "#000000"
            }

           minorTickmark: Rectangle {
                visible: styleData.value < 360
                implicitWidth: outerRadius * 0.01
                antialiasing: true
                implicitHeight: outerRadius * 0.03
                color: "#000000"
           }

           tickmarkLabel:  Text {
                font.pixelSize: Math.max(6, outerRadius * 0.1)
                text: styleData.value
                color: styleData.value >= 360 ? "#000000" : "#000000"
                antialiasing: true
           }

           needle: Rectangle {
                y: outerRadius * 0.15
                implicitWidth: outerRadius * 0.03
                implicitHeight: outerRadius * 1.1
                antialiasing: true
                color: "#000000"
           }

           foreground: Item {
                Rectangle {
                     width: outerRadius * 0.2
                     height: width
                     radius: width / 2
                     color: "#b2b2b2"
                     anchors.centerIn: parent
                }
           }
      }
 }
}
