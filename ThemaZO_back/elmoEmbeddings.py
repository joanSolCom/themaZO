from elmoformanylangs import Embedder
import numpy as np
from scipy.spatial.distance import cdist

class ElmoEmbeddings:
	def __init__(self, modelPath="/home/joan/Escritorio/ELMoForManyLangs-master/EN/"):
		self.elmo = Embedder(modelPath)

	def getSentenceVector(self, sentence):
		vecs = self.elmo.sents2elmo(sentence)
		vectorList = []
		for vec in vecs:
			vectorList.append(vec[0].tolist())

		return vectorList

	def getCentroid(self, vectors):
		avgVector = np.mean(vectors,axis=0)
		return avgVector.tolist()

	def distance(self, A, B, distance = "cosine"):
		return cdist([A],[B],distance)