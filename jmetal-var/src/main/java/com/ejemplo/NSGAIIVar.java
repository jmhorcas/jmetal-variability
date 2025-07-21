package com.ejemplo;

import java.io.IOException;
import java.util.List;
import java.util.Arrays;
import java.util.Comparator;
import org.uma.jmetal.component.algorithm.EvolutionaryAlgorithm;
import org.uma.jmetal.component.catalogue.common.solutionscreation.SolutionsCreation;
import org.uma.jmetal.component.catalogue.common.solutionscreation.impl.RandomSolutionsCreation;
import org.uma.jmetal.component.catalogue.common.evaluation.Evaluation;
import org.uma.jmetal.component.catalogue.common.evaluation.impl.SequentialEvaluation;
import org.uma.jmetal.component.catalogue.common.termination.Termination;
import org.uma.jmetal.component.catalogue.common.termination.impl.TerminationByEvaluations;
import org.uma.jmetal.component.catalogue.ea.replacement.Replacement;
import org.uma.jmetal.component.catalogue.ea.replacement.impl.RankingAndDensityEstimatorReplacement;
import org.uma.jmetal.component.catalogue.ea.selection.Selection;
import org.uma.jmetal.component.catalogue.ea.selection.impl.NaryTournamentSelection;
import org.uma.jmetal.component.catalogue.ea.variation.Variation;
import org.uma.jmetal.component.catalogue.ea.variation.impl.CrossoverAndMutationVariation;
import org.uma.jmetal.operator.crossover.CrossoverOperator;
import org.uma.jmetal.operator.crossover.impl.SBXCrossover;
import org.uma.jmetal.operator.mutation.MutationOperator;
import org.uma.jmetal.operator.mutation.impl.PolynomialMutation;
import org.uma.jmetal.problem.Problem;
import org.uma.jmetal.problem.ProblemFactory;
import org.uma.jmetal.solution.Solution;
import org.uma.jmetal.solution.doublesolution.DoubleSolution;
import org.uma.jmetal.util.comparator.MultiComparator;
import org.uma.jmetal.util.densityestimator.DensityEstimator;
import org.uma.jmetal.util.densityestimator.impl.CrowdingDistanceDensityEstimator;
import org.uma.jmetal.util.ranking.Ranking;
import org.uma.jmetal.util.ranking.impl.FastNonDominatedSortRanking;
import org.uma.jmetal.util.restartstrategy.CreateNewSolutionsStrategy;
import org.uma.jmetal.util.JMetalLogger;
import org.uma.jmetal.util.comparator.dominanceComparator.impl.GDominanceComparator;
import org.uma.jmetal.util.errorchecking.JMetalException;
import org.uma.jmetal.util.fileoutput.SolutionListOutput;
import org.uma.jmetal.util.fileoutput.impl.DefaultFileOutputContext;
import org.uma.jmetal.util.pseudorandom.JMetalRandom;
import org.uma.jmetal.util.SolutionListUtils;
import org.uma.jmetal.util.VectorUtils;
import org.uma.jmetal.qualityindicator.QualityIndicatorUtils;


public class NSGAIIVar {

  public static void main(String[] args) throws JMetalException, IOException {
    // Problem configuration
    String problemName = "org.uma.jmetal.problem.multiobjective.zdt.ZDT1";
    String referenceParetoFront = "resources/referenceFrontsCSV/ZDT1.csv";

    Problem<DoubleSolution> problem = ProblemFactory.<DoubleSolution>loadProblem(problemName);

    // Algorithm configuration
    String algorithmName = "NSGAII";

    // Configure initial population creation
    int populationSize = 100;
    SolutionsCreation<DoubleSolution> createInitialPopulation = new RandomSolutionsCreation<>(problem, populationSize);

    // Configure evaluation
    Evaluation<DoubleSolution> evaluation = new SequentialEvaluation<>(problem);

    // Configure termination condition
    Termination termination = new TerminationByEvaluations(25000);

    // Configure the crossover operator
    double crossoverProbability = 0.9;
    SBXCrossover crossover = new SBXCrossover(crossoverProbability);
    crossover.distributionIndex(20.0);

    // Configure the mutation operator
    double mutationProbability = 1.0 / problem.numberOfVariables();
    PolynomialMutation mutation = new PolynomialMutation(mutationProbability);
    mutation.setDistributionIndex(20.0);

    // Configure replacement
    Ranking<DoubleSolution> ranking = new FastNonDominatedSortRanking<>();
    DensityEstimator<DoubleSolution> densityEstimator = new CrowdingDistanceDensityEstimator<>();
    Replacement<DoubleSolution> replacement = new RankingAndDensityEstimatorReplacement<>(ranking, densityEstimator, Replacement.RemovalPolicy.ONE_SHOT);

    // Configure variation
    int offspringPopulationSize = 100;
    Variation<DoubleSolution> variation = new CrossoverAndMutationVariation<>(offspringPopulationSize, crossover, mutation);

    // Configure selection operator
    int tournamentSize = 2;
    Selection<DoubleSolution> selection = new NaryTournamentSelection<>(
            tournamentSize,
            variation.getMatingPoolSize(),
            new MultiComparator<>(
                Arrays.asList(
                    Comparator.comparing(ranking::getRank),
                    Comparator.comparing(densityEstimator::value).reversed())));

    EvolutionaryAlgorithm<DoubleSolution> nsgaii = new EvolutionaryAlgorithm<>(
      algorithmName, 
      createInitialPopulation, 
      evaluation, 
      termination,
      selection, 
      variation, 
      replacement);

    // Run the algorithm
    nsgaii.run();

    List<DoubleSolution> population = nsgaii.result();
    JMetalLogger.logger.info("Total execution time : " + nsgaii.totalComputingTime() + "ms");
    JMetalLogger.logger.info("Number of evaluations: " + nsgaii.numberOfEvaluations() + "\n");

    new SolutionListOutput(population)
        .setVarFileOutputContext(new DefaultFileOutputContext("VAR.csv", ","))
        .setFunFileOutputContext(new DefaultFileOutputContext("FUN.csv", ","))
        .print();

    JMetalLogger.logger.info("Random seed: " + JMetalRandom.getInstance().getSeed());
    JMetalLogger.logger.info("Objectives values have been written to file FUN.csv");
    JMetalLogger.logger.info("Variables values have been written to file VAR.csv");

    QualityIndicatorUtils.printQualityIndicators(
        SolutionListUtils.getMatrixWithObjectiveValues(population),
        VectorUtils.readVectors(referenceParetoFront, ","));
  }
}