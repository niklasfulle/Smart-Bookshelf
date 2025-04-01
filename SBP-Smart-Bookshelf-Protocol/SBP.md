# Grundschicht

| Bytes     | Inhalt          |
| :-------- | :-------------- |
| 2 Bytes   | Länge           |
| 4 Bytes   | Sequenznr.      |
| n Bytes   | Nutzdaten       |
| 6 + n + 8 | Sicherheitscode |

# Paketschicht

### Nachrichtentype

| Nachrichtentype | Bedeutung             | Englische Bezeichnung  | Abkürzung      |
| :-------------- | :-------------------- | :--------------------- | :------------- |
| 3000            | Verbindungsanfrage    | Connection Request     | ConnRequest    |
| 3010            | Verbindungsantwort    | Connection Response    | ConnResponse   |
| 3020            | Verbindungszustimmung | Connection Approve     | ConnApprove    |
| 3030            | Versionsanfrage       | Version Request        | VerRequest     |
| 3040            | Versionsantwort       | Version Response       | VerResponse    |
| 3050            | Statusanfrage         | Status Request         | StatusRequest  |
| 3060            | Statusantwort         | Status Response        | StatusResponse |
| 3070            | Trennaufforderung     | Disconnection Request  | DiscRequest    |
| 3080            | Trennantwort          | Disconnection Response | DiscResponse   |
| 3090            | Schlafaufforderung    | Sleep Request          | SleepRequest   |
| 3100            | Schlafantwort         | Sleep Response         | SleepResponse  |
| 3110            | Neustartaufforderung  | Reboot Request         | RebootRequest  |
| 3120            | Neustartantwort       | Reboot Response        | RebootResponse |
| 5000            | Daten                 | Data                   | Data           |
| 6000            | Daten Hochladen       | Upload data            | DataUpload     |

<br>
<b>Verbindungsanfragenachricht (Connection Request Message)</b>

| Byte Nr. | Inhalt                       |
| :------: | :--------------------------- |
| 00 - 01  | Nachrichtenlänge = 36        |
| 02 - 03  | Nachrichtentyp = 3000        |
| 04 - 07  | Empfängerkennung             |
| 08 - 11  | Absenderkennung              |
| 12 - 15  | Sequenznummer                |
| 16 - 19  | Bestätigte Sequenznummer = 0 |
| 20 - 23  | Zeitstempel                  |
| 24 - 27  | Bestätigter Zeitstempel = 0  |
| 28 - 35  | Sicherheitscode              |

<br>
<b>Verbindungsantwortnachricht (Connection Response Message)</b>

| Byte Nr. | Inhalt                       |
| :------: | :--------------------------- |
| 00 - 01  | Nachrichtenlänge = 36        |
| 02 - 03  | Nachrichtentyp = 3010        |
| 04 - 07  | Empfängerkennung             |
| 08 - 11  | Absenderkennung              |
| 12 - 15  | Sequenznummer                |
| 16 - 19  | Bestätigte Sequenznummer = 0 |
| 20 - 23  | Zeitstempel                  |
| 24 - 27  | Bestätigter Zeitstempel = 0  |
| 28 - 35  | Sicherheitscode              |

<br>
<b>Verbindungszustimmungsnachricht (Connection Approve Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3020    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Versionsanfragenachricht (Version Request Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3030    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Versionsantwortnachricht (Version Response Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 43    |
| 02 - 03  | Nachrichtentyp = 3040    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 29  | Protokollversion         |
| 30 - 31  | Configversion            |
| 32 - 33  | Bookshelfsversion        |
| 34 - 42  | Sicherheitscode          |

<br>
<b>Statusanfragenachricht (Status Request Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3050    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Statusantwortnachricht (Status Response Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 38    |
| 02 - 03  | Nachrichtentyp = 3060    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 29  | Status                   |
| 30 - 37  | Sicherheitscode          |

<br>
<b>Trennaufforderungsnachricht (Disconnect Request Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 38    |
| 02 - 03  | Nachrichtentyp = 3070    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 29  | Grund                    |
| 30 - 37  | Sicherheitscode          |

<br>
<b>Trennaufforderungsnachricht (Disconnect Response Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 38    |
| 02 - 03  | Nachrichtentyp = 3080    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 29  | Grund                    |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Schlafaufforderungsnachricht (Sleep Request Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3090    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Schlafaufforderungsnachricht (Sleep Response Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3100    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Neustartaufforderungsnachricht (Reboot Request Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3110    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Neustartaufforderungsnachricht (Reboot Response Message)</b>

| Byte Nr. | Inhalt                   |
| :------: | :----------------------- |
| 00 - 01  | Nachrichtenlänge = 36    |
| 02 - 03  | Nachrichtentyp = 3120    |
| 04 - 07  | Empfängerkennung         |
| 08 - 11  | Absenderkennung          |
| 12 - 15  | Sequenznummer            |
| 16 - 19  | Bestätigte Sequenznummer |
| 20 - 23  | Zeitstempel              |
| 24 - 27  | Bestätigter Zeitstempel  |
| 28 - 35  | Sicherheitscode          |

<br>
<b>Datennachricht (Data Message)</b>

|         Byte Nr.         | Inhalt                    |
| :----------------------: | :------------------------ |
|         00 - 01          | Nachrichtenlänge = 36 + n |
|         02 - 03          | Nachrichtentyp = 5000     |
|         04 - 07          | Empfängerkennung          |
|         08 - 11          | Absenderkennung           |
|         12 - 15          | Sequenznummer             |
|         16 - 19          | Bestätigte Sequenznummer  |
|         20 - 23          | Zeitstempel               |
|         24 - 27          | Bestätigter Zeitstempel   |
|     28 - 28 + n – 1      | n Bytes Nutzdaten         |
| 28 + n - 28 + <br> n + 7 | Sicherheitscode           |

<br>
<b>Datenhochladennachricht (Upload data Message)</b>

|         Byte Nr.         | Inhalt                    |
| :----------------------: | :------------------------ |
|         00 - 01          | Nachrichtenlänge = 36 + n |
|         02 - 03          | Nachrichtentyp = 6000     |
|         04 - 07          | Empfängerkennung          |
|         08 - 11          | Absenderkennung           |
|         12 - 15          | Sequenznummer             |
|         16 - 19          | Bestätigte Sequenznummer  |
|         20 - 23          | Zeitstempel               |
|         24 - 27          | Bestätigter Zeitstempel   |
|     28 - 28 + n – 1      | n Bytes Nutzdaten         |
| 28 + n - 28 + <br> n + 7 | Sicherheitscode           |

# Datenschicht

### Nachrichtentype

| Nachrichtentype | Bedeutung         | Englische Bezeichnung | Abkürzung    |
| :-------------- | :---------------- | :-------------------- | :----------- |
| 5001            | Licht einschalten | Switch on light       | ShowOnLight  |
| 5002            | Licht ausschalten | Switch off light      | ShowOffLight |
| 5003            | Buch zeigen       | Show book             | ShowBook     |
| 5004            | Bücher zeigen     | Show books            | ShowBooks    |
| 5020            | Licht Modus       | Light mode            | LightMode    |

<br>
<b>Lichteinschaltennachricht (Switch on light Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge =    |
| 02 - 03  | Nachrichtentyp = 5001 |

<br>
<b>Lichtausschaltennachricht (Switch off light Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge =    |
| 02 - 03  | Nachrichtentyp = 5002 |

<br>
<b>Buchzeigennachricht (Show book Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge =    |
| 02 - 03  | Nachrichtentyp = 5003 |
| 04 - 07  | Buch Postion          |

<br>
<b>Bücherzeigennachricht (Show books Message)</b>

| Byte Nr.  | Inhalt                |
| :-------: | :-------------------- |
|  00 - 01  | Nachrichtenlänge =    |
|  02 - 03  | Nachrichtentyp = 5004 |
|  04 - 07  | Buch Postion          |
|  08 - 11  | Buch Postion          |
| n - n + 1 | Buch Postion          |

<br>
<b>Lichtmodusnachricht (Light mode Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge =    |
| 02 - 03  | Nachrichtentyp = 5020 |
|    04    | Modus                 |

# Datenuploadschicht

### Nachrichtentype

| Nachrichtentype | Bedeutung                     | Englische Bezeichnung | Abkürzung |
| :-------------- | :---------------------------- | :-------------------- | :-------- |
| 6001            | Daten hochladen Starten       | Upload data Start     | DataUpSta |
| 6002            | Daten hochladen               | Upload data           | DataUp    |
| 6003            | Daten hochladen Abgeschlossen | Upload data Completed | DataUpCom |
| 6004            | Daten hochladen Fehler        | Upload data Error     | DataUpErr |
| 6005            | Daten hochladen Abbrechen     | Upload data Cancel    | DataUpCan |

<br>
<b>Datenhochladenstartnachricht (Start uploading data Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge = 4  |
| 02 - 03  | Nachrichtentyp = 6001 |
| 04 - 05  | Datentyp              |

<br>
<b>Datenhochladennachricht (Upload data Message)</b>

|     Byte Nr.     | Inhalt                        |
| :--------------: | :---------------------------- |
|     00 - 01      | Nachrichtenlänge = 7 + n < 88 |
|     02 - 03      | Nachrichtentyp = 6002         |
|     04 - 05      | Datenpaket Nummer             |
| 06 - 06 + n < 88 | Datenpaket                    |

<br>
<b>Datenbestätigungsnachricht (Upload confirm Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge = 6  |
| 02 - 03  | Nachrichtentyp = 6003 |
| 04 - 05  | Datenpaket Nummer     |

<br>
<b>Datenhochladenabgeschlossennachricht (Upload data Completed Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge = 4  |
| 02 - 03  | Nachrichtentyp = 6004 |

<br>
<b>Datenhochladenfehlernachricht (Upload data Error Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge = 5  |
| 02 - 03  | Nachrichtentyp = 6005 |
|    04    | Fehler                |

<br>
<b>Datenhochladenabbrechennachricht (Upload data Cancel Message)</b>

| Byte Nr. | Inhalt                |
| :------: | :-------------------- |
| 00 - 01  | Nachrichtenlänge = 4  |
| 02 - 03  | Nachrichtentyp = 6006 |
