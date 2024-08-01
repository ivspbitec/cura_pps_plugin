from ..Script import Script

class ModifyFlowRateOnLayer(Script):
    def getSettingDataString(self):
        return """{
            "name": "01 Modify Flow Rate On Layer",
            "key": "ModifyFlowRateOnLayer",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "flow_rate_layer_2":
                {
                    "label": "Flow Rate for Layer 2 (%)",
                    "description": "Set the flow rate for the second layer.",
                    "type": "float",
                    "default_value": 100
                },
                "flow_rate_layer_3":
                {
                    "label": "Flow Rate for Layer 3 (%)",
                    "description": "Set the flow rate for the third layer.",
                    "type": "float",
                    "default_value": 100
                },
                "flow_rate_layer_4":
                {
                    "label": "Flow Rate for Layer 4 (%)",
                    "description": "Set the flow rate for the fourth layer.",
                    "type": "float",
                    "default_value": 100
                },
                "flow_rate_layer_all":
                {
                    "label": "Flow Rate for All other Layers",
                    "description": "Set the flow rate all other layers.",
                    "type": "float",
                    "default_value": 120
                }
            }
        }"""

    def execute(self, data):
        flow_rate_layer_2 = self.getSettingValueByKey("flow_rate_layer_2")
        flow_rate_layer_3 = self.getSettingValueByKey("flow_rate_layer_3")
        flow_rate_layer_4 = self.getSettingValueByKey("flow_rate_layer_4")
        flow_rate_layer_all = self.getSettingValueByKey("flow_rate_layer_all")
        
        layer_count = -1
        inside_skin = False

        for i in range(len(data)):
            lines = data[i].split("\n")

            for j in range(len(lines)):
                if inside_skin and (";TYPE:" in lines[j] or ";LAYER:" in lines[j] ):
                    inside_skin = False
                    lines.insert(j, "M221 S100")  

                if ";LAYER:" in lines[j]:
                    layer_count += 1
                    inside_skin = False

                if ";TYPE:SKIN" in lines[j]:
                    if layer_count == 1:
                        lines.insert(j + 1, f"M221 S{flow_rate_layer_2}")
                        inside_skin = True    
                    elif layer_count == 2:
                        lines.insert(j + 1, f"M221 S{flow_rate_layer_3}")
                        inside_skin = True    
                    elif layer_count == 3:
                        lines.insert(j + 1, f"M221 S{flow_rate_layer_4}")
                        inside_skin = True    
                    elif layer_count != 0:
                        lines.insert(j + 1, f"M221 S{flow_rate_layer_all}") 
                        inside_skin = True    

            data[i] = "\n".join(lines)

        return data
