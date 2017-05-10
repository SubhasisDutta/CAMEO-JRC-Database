import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.SparkContext
import org.apache.spark.mllib.tree.DecisionTree
import org.apache.spark.mllib.tree.configuration.Algo._
import org.apache.spark.mllib.tree.impurity.Gini

object classification {
    def main(args: Array[String]) = {
      val conf = new SparkConf().setAppName("Naive Bayes").setMaster("local[1]")
      val sc = new SparkContext(conf)
      
      val train = sc.textFile("snr150130/BD/final-train.csv")
      val test = sc.textFile("snr150130/BD/final-test.csv")

      val training = train.map { line =>
        val parts = line.split(",")
        LabeledPoint(parts(7).toDouble, Vectors.dense(parts(2).toDouble,parts(3).toDouble,parts(4).toDouble,parts(5).toDouble,parts(6).toDouble,parts(7).toDouble))
      }.cache()

     /* val splits = training.randomSplit(Array(0.6, 0.4))
     val train1 = splits(0)
      val test1 = splits(1)*/
      val testing = test.map { line =>
        val parts = line.split(",")
        LabeledPoint(parts(7).toDouble, Vectors.dense(parts(2).toDouble,parts(3).toDouble,parts(4).toDouble,parts(5).toDouble,parts(6).toDouble,parts(7).toDouble))
      }.cache()

      val model = NaiveBayes.train(training, lambda = 1.0)

      val predictionAndLabel = testing.map(p => (p.label, model.predict(p.features)))
      predictionAndLabel.foreach(println)
      val accuracy = 1.0 * predictionAndLabel.filter(x => x._1 == x._2).count() / test.count()

      println("Accuracy of Naive Bayes - " + accuracy)
    }
}