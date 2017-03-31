
trainindex<-sample(1:nrow(entities),0.8*nrow(entities))
train<-mydat[trainindex, ]
test<-mydat[-trainindex, ]

> train <- read_delim("~/study materials/Independent Study/train.txt","\t", escape_double = FALSE, trim_ws = TRUE)
Parsed with column specification:
cols(
  `1000238` = col_integer(),
  P = col_character(),
  de = col_character(),
  Allianz = col_character()
)
> test <- read_delim("~/study materials/Independent Study/test.txt", "\t", escape_double = FALSE, trim_ws = TRUE)
Parsed with column specification:
cols(
  `1001293` = col_integer(),
  P = col_character(),
  u = col_character(),
  `Babacar+Ndiour` = col_character()
)
> test <- read_delim("~/study materials/Independent Study/test.txt", "\t", escape_double = FALSE, trim_ws = TRUE)
Parsed with column specification:
cols(
  `1001293` = col_integer(),
  P = col_character(),
  u = col_character(),
  `Babacar+Ndiour` = col_character()
)
> 

> colnames(test)= c("line_number","entity_type","language","name_variant")
> colnames(train)= c("line_number","entity_type","language","name_variant")
> library(e1071)

> Class1<-as.matrix(train[,as.character("language")])
> Class<-as.factor(Class1)
> model <- naiveBayes(Class ~ ., data = train)
> pred <- predict(model, matrix(as.numeric(unlist(test)),nrow=nrow(test)))
Warning message:
In matrix(as.numeric(unlist(test)), nrow = nrow(test)) :
  NAs introduced by coercion
> pred <- predict(model, matrix(as.character(unlist(test)),nrow=nrow(test)))
> accr <- sum(pred == Class[-trainindex])/length(pred)
Error in NextMethod("[") : object 'trainindex' not found
> accr <- sum(pred == Class[84])/length(pred)
> cat(sprintf("\t Naive Bayesian Classifier: \t \t \t %f \n",accr*100))
	 Naive Bayesian Classifier: 	 	 	 100.000000 