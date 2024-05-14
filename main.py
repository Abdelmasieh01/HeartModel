from PyQt5.QtCore import Qt, QTimer, QVariant, QPointF, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import math

from AFlutterData import AFlutterData as Data

from Heart import Heart

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    url = "qrc:/main.qml"

    def object_created(obj, objUrl):
        if not obj and url == objUrl:
            app.quit()

    engine.objectCreated.connect(object_created)

    engine.load(url)

    heart_model = Heart.getInstance()
    color_opt_node = ["lime", "red", "yellow"]
    color_opt_path = ["blue", "lime", "yellow", "black", "red"]

    nodeList = []
    for i in range(len(Data.node_names)):
        nodeList.append({"x": Data.node_positions[i][0],
                         "y": Data.node_positions[i][1],
                         "c": "yellow"})

    pathList = []
    for i in range(len(Data.path_names)):
        ent_x = Data.node_positions[Data.path_int_parameters[i][1] - 1][0]
        ent_y = Data.node_positions[Data.path_int_parameters[i][1] - 1][1]
        out_x = Data.node_positions[Data.path_int_parameters[i][2] - 1][0]
        out_y = Data.node_positions[Data.path_int_parameters[i][2] - 1][1]
        degree = 180 / math.pi * math.atan2(out_y - ent_y, out_x - ent_x)
        if ent_x > out_x:
            if ent_y > out_y:
                degree = abs(degree)
            else:
                degree = -abs(degree)
        else:
            if ent_y > out_y:
                degree = abs(degree)
            else:
                degree = 360 - abs(degree)
        len_val = math.sqrt((out_x - ent_x)**2 + (out_y - ent_y)**2)
        pathList.append({"x": ent_x,
                         "y": ent_y,
                         "c": "blue",
                         "l": len_val,
                         "d": degree})

    # rootObject = engine.rootObjects()[0]
    rootObject = QObject()
    if rootObject is not None:
        timer = QTimer(rootObject)
        delay = 10
        index = 0

        paths_nodes_names = [Data.path_names[i] for i in range(len(Data.path_names))]
        rootObject.setProperty("pathsNames", QVariant(paths_nodes_names))
        # rootObject.setProperty("pathsNames", QVariant.fromValue(paths_nodes_names))
        paths_nodes_names = [Data.node_names[i] for i in range(len(Data.node_names))]
        rootObject.setProperty("nodesNames", QVariant(paths_nodes_names))
        # rootObject.setProperty("nodesNames", QVariant.fromValue(paths_nodes_names))

        def on_timeout():
            index = 0
            if index < 10000000:  # Data.node_positions.size()
                rootObject.setProperty("timerLabel", index)
                heart_model.heart_automaton()
                for i, originalNode in enumerate(nodeList):
                    modifiedElement = originalNode.copy()
                    modifiedElement["c"] = color_opt_node[
                        heart_model.getNodeTable().node_table[i].getParameters().node_state_index - 1]
                    nodeList[i] = modifiedElement
                for i, originalPath in enumerate(pathList):
                    modifiedElement = originalPath.copy()
                    psi = heart_model.getPathTable().path_table[i].getParameters().path_state_index - 1
                    modifiedElement["c"] = color_opt_path[psi]
                    pathList[i] = modifiedElement
                rootObject.setProperty("pointData", QVariant(nodeList))
                rootObject.setProperty("pathData", QVariant(pathList))
                # rootObject.setProperty("pointData", QVariant.fromValue(nodeList))
                # rootObject.setProperty("pathData", QVariant.fromValue(pathList))
                index += 1
            else:
                timer.stop()
                print("END OF 100'000 cycle")

        timer.timeout.connect(on_timeout)
        timer.start(delay)

    sys.exit(app.exec_())
