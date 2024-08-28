# pml_download
This app  downloads wholesale electricity prices by Node in Mexico by connecting to the CENACE API (Mexican Independent System Operator).

The app takes as parameters:
- Sistema eléctrico: SIN, BCA, BCS.
- Mercado: MDA,MTR
- Lista de nodos de los cuales se desea obtener información (La lista de nodos debe ser separada por comas sin espacio).
- Año inicial, para un periodo de tiempo. Formato AAAA
- Mes inicial, para un periodo de tiempo. Formato MM
- Día Inicial, para un periodo de tiempo. Formato DD
- Año final, para un periodo de tiempo. Formato AAAA
- Mes final, para un periodo de tiempo. Formato MM
- Día final, para un periodo de tiempo. Formato DD
- Formato de salida XML o JSON, por omisión es XML (Opcional)

The resulting hourly prices are stored in an excel file, please see PMLs01CTT-85-20220401-20220430.xlsx as an example of the output file

Please refer to Manual para Uso SW-PML 2018 03 01 v2.pdf for more information on how the API works.
