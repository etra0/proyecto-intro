>Consejos para usar git desde la terminal:
>
>primero, obvio llegar a la carpeta del proyecto.
>Cuándo hagan una modificación del archivo, lo guardan y van en este orden:
>>
>>**git add *nombreArchivo* ** Avisas que van a agregar
>>
>>**git commit -m *"resumen modificacion"* ** Con esto comentan lo que hicieron
>>
>>**git push origin master** Ahi lo subes a la pagina
>
>Si quieren empezar un código por separado, es conveniente crear una rama (branch)
>
>>**git branch *nombreRama* ** para crear la rama
>>
>>**git checkout *nombreRama* ** Para situarse en la rama, y después hacen lo mismo que arriba
>
>>**git add *nombreArchivo* **
>>
>>**git commit -m *"resumen"* **
>>
>>**git push origin *nombreRama* ** aqui cambian master por **nombreRama**, importante!
>
>
>
>Si quieren ver los cambios desde la terminal:
>>**git log**
>
>cambios resumidos:
>>**git log --oneline --decorate**