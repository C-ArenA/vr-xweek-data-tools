# Notes for myself

## Open Windows Terminal from VsCode

I like to use the windows terminal, but VSCODE initializes the venv automatically
so I decided to run the following command insidethe integrated cmd terminal of VSCODE:

```bash
wt.exe -d .
```

Si se desea abrir en un "cmd" dentro del Windows Terminal:

```bash
wt.exe -d . -p "cmd"
```
## Stack Overflow

No se le puede pasar un evento completo a Restaurant, porque en verdad es el Restaurant
el que debe de hacerse de un objeto con un id. El evento no pueede modificarse
desded Restaurant, a excepción del atributyo restaurants

Tuve el problema de que estaban muy acopladas mis clases y se hacía un loop infinito
APRENDÍ : Si Event está por encima de Restaurant, mejor dejo que se controle a Restaurant
desde Event y no a Event desde Restaurant

## Inspiration

The structure of this project was inspired by the following open source project:
[Nagstamon](https://github.com/HenriWahl/Nagstamon/blob/master/Nagstamon/Helpers.py)
I write it down 'cause reading that project's code made me understand some stuff in
Python that I didn't before (like the way the imports work in a mediume to big project)

I found Nagstamos in [this](https://github.com/mahmoud/awesome-python-applications#tag-education) list of open source Python projects

## NOTES
* debo implemetnar una funcionalidad para arrastrar las imágenes por restaurante y por evento
* En el sitio debo usar shortcodes