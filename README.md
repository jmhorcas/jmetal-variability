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