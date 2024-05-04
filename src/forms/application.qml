import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    title: "Hello, QML!"

    Button {
        margin: {
            left: 10
            top: 10
        }
        text: "Click me"
        onClicked: console.log("Button clicked")
    }
}
