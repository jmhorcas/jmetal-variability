# jmetal-variability

## How to

1. Download [jMetal](https://github.com/jMetal/jMetal.git) source code:
    `git clone https://github.com/jMetal/jMetal.git`
2. Install jMetal with Maven: 
    `mvn clean install -Dgpg.skip=true -DskipTests=true`
3. Download this repository: 
    `git clone https://github.com/jmhorcas/jmetal-variability.git`
4. Update the jMetal's version dependency (if needed) with the version indicated in the `pom.xml` of the downloaded jMetal repository.
    ```
    <dependency>
        <groupId>org.uma.jmetal</groupId>
        <artifactId>jmetal</artifactId>
        <version>6.7-SNAPSHOT</version>
    </dependency>
    ```
5. Execute the example:
    `AppExample`


## Tips para implementar mejor la variabilidad
- El parámetro común de todos los crossover es el "crossover probability". Por lo tanto, todos los crossover deberían tener un constructor que reciba solo el crossover probability.
- Para el resto de parámetros, se añade un setter y opcionalmente un constructor (si no hay valor por defecto).
- Si hay valor por defecto, el constructor es opcional.