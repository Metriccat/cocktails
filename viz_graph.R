# data exploration for the cocktails database

#devtools::install_github("garthtarr/edgebundleR")
library(edgebundleR)
library(igraph)
library(plyr)
library(wordcloud)
library(networkD3)
library(reshape2)

# clean returns: tr -d $'\r' < cocktails_thecocktaildb_ingredients_split.csv > output.csv
data = read.csv("path/to/cocktails_thecocktaildb_ingredients_split.csv", sep="#", stringsAsFactors = FALSE, header=T)
head(data)

test = sapply(data$ingredients_nodosage, function(s) strsplit(s,","))
names(test) = NULL
head(test)
test = Filter(function(x) length(x) > 1, test) # some recipes have 1 ingredient ? prb with fetching ... TODO

# ye olde wordcloud 
all_words = count(melt(test)[,1])
wordcloud(all_words[,1], all_words[,2])

# graph of relationships
# edge exists when ingredients appear together in a list, edge weight = total number of coappearances
all_edges = sapply(test, FUN=function(l) combn(l,2))
all_edges_df_all = data.frame(t(do.call(cbind, all_edges))) # error with dplyr bind_cols (?)
all_edges_df_all$X1 = as.character(all_edges_df_all$X1)
all_edges_df_all$X2 = as.character(all_edges_df_all$X2)
# remove very rare ingredients
rare_ingredients = as.character(all_words$x[all_words$freq < 10])
all_edges_df = all_edges_df_all[!all_edges_df_all$X1 %in% rare_ingredients & !all_edges_df_all$X2 %in% rare_ingredients, ]
edges_weights = count(all_edges_df)
names(edges_weights) = c("source", "target", "weight")
edges_weights$source = as.character(edges_weights$source)
edges_weights$target = as.character(edges_weights$target)

g = graph.data.frame(edges_weights, directed=F)

# edgebundle does not show weights
edgebundle(g)

# networkD3: force graphs
simpleNetwork(edges_weights, fontSize = 16) # no edge weights; slows computer already with 22 nodes

nodes = unique(c(edges_weights$source, edges_weights$target))
nodes
lookup = setNames(1:length(nodes)-1, nodes)

nodes_df = data.frame("name" = nodes, "id" = lookup)

links_df = data.frame("source" = sapply(edges_weights$source, function(s) lookup[s]),
                      "target" = sapply(edges_weights$target, function(s) lookup[s]),
                      "weight" = edges_weights$weight)

forceNetwork(Links = links_df, Nodes = nodes_df,
             Source = "source", Target = "target",
             Value = "weight", NodeID = "name", Group="id", 
             opacity = 0.8, fontSize = 16, zoom=TRUE,
             linkWidth=JS("function(d) { return Math.abs(d.value); }"))

