# SAND BOX

sb-7ysfq8935004@business.example.com - Email
AXNerpSeUK2z2O5B3ogz1vH-3faY-oNH-64furHQ0jLbQpqZC8Zb0BB2OBVN7g3MiDz1TFLoV43qMP9i    CLIENT ID
EHMGuwUrazotq0m568SgN70ifhRm1g85xvPiXbnpDFVwGWeY-rV7DJ1HC3i7s2tAVLF1_GaTdU8Yzaue	SECRET


# Zásilkovna 

https://client.packeta.com/cs/support/?backlink=hirar
7a4645e0fcf8f51f - API klíč
7a4645e0fcf8f51fe038e6044b1e100d - API heslo

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script src="https://widget.packeta.com/v6/www/js/library.js"></script>
    <script>
        var packetaApiKey = '7a4645e0fcf8f51f';
        /*
        	This function will receive either a pickup point object, or null if the user
        	did not select anything, e.g. if they used the close icon in top-right corner
        	of the widget, or if they pressed the escape key.
        */
        function showSelectedPickupPoint(point) {
            var spanElement = document.getElementById('packeta-point-info');
            var idElement = document.getElementById('packeta-point-id');
            if (point) {
                var recursiveToString = function(o) {
                    return Object.keys(o).map(
                        function(k) {
                            if (o[k] === null) {
                                return k + " = null";
                            }

                            return k + " = " + (typeof(o[k]) == "object" ?
                                "<ul><li>" + recursiveToString(o[k]) + "</li></ul>" :
                                o[k].toString().replace(/&/g, '&amp;').replace(/</g, '&lt;')
                            );
                        }
                    ).join("</li><li>");
                };

                spanElement.innerText =
                    "Address: " + point.name + "\n" + point.zip + " " + point.city + "\n\n" +
                    "All available fields:\n";

                spanElement.innerHTML +=
                    "<ul><li>" + recursiveToString(point) + "</li></ul>";

                idElement.value = point.id;
            } else {
                spanElement.innerText = "None";
                idElement.value = "";
            }
        };
        </script>
</head>
<body>
    <input type="button" onclick="Packeta.Widget.pick(packetaApiKey, showSelectedPickupPoint)" value="Select pick-up point...">
    <p>Selected point:
        <input type="hidden" id="packeta-point-id">
        <span id="packeta-point-info">None</span>
    </p>
    
</body>
</html>
```
