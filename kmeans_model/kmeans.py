class KMeans:
    def __init__(self, n_clusters, max_iter=100, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol

    def _validate_X(self, X):
        if X is None or len(X) == 0:
            raise ValueError("X must be a non-empty sequence of points")
        if not isinstance(self.n_clusters, int) or self.n_clusters <= 0:
            raise ValueError("n_clusters must be a positive integer")
        if self.n_clusters > len(X):
            raise ValueError("n_clusters must be <= number of points in X")

        first = X[0]
        if first is None:
            raise ValueError("X contains invalid point")
        try:
            dim = len(first)
        except Exception as e:
            raise ValueError("Each point in X must be a sequence") from e
        if dim == 0:
            raise ValueError("Points must have at least one dimension")

        for i, p in enumerate(X):
            if p is None:
                raise ValueError("X contains invalid point")
            try:
                if len(p) != dim:
                    raise ValueError("All points must have the same dimension")
            except TypeError as e:
                raise ValueError("Each point in X must be a sequence") from e
        return dim

    @staticmethod
    def _squared_euclidean(a, b):
        s = 0.0
        for i in range(len(a)):
            d = a[i] - b[i]
            s += d * d
        return s

    def _assign_labels(self, X, centroids):
        labels = []
        for x in X:
            best_k = 0
            best_dist = self._squared_euclidean(x, centroids[0])
            for k in range(1, len(centroids)):
                dist = self._squared_euclidean(x, centroids[k])
                if dist < best_dist:
                    best_dist = dist
                    best_k = k
            labels.append(best_k)
        return labels

    @staticmethod
    def _mean_of_points(points, dim):
        sums = [0.0] * dim
        for p in points:
            for j in range(dim):
                sums[j] += p[j]
        n = float(len(points))
        return [s / n for s in sums]

    def fit(self, X):
        dim = self._validate_X(X)

        # Deterministic initialization: shallow copies of first n_clusters points
        centroids = [list(X[i]) for i in range(self.n_clusters)]

        labels = None
        for _ in range(self.max_iter):
            labels = self._assign_labels(X, centroids)

            # Group points by cluster
            clusters = [[] for _ in range(self.n_clusters)]
            for x, lab in zip(X, labels):
                clusters[lab].append(x)

            new_centroids = []
            for k in range(self.n_clusters):
                if clusters[k]:
                    new_centroids.append(self._mean_of_points(clusters[k], dim))
                else:
                    # Empty cluster: keep previous centroid
                    new_centroids.append(centroids[k])

            # Check convergence by maximum centroid shift
            max_shift = 0.0
            for old, new in zip(centroids, new_centroids):
                shift = self._squared_euclidean(old, new) ** 0.5
                if shift > max_shift:
                    max_shift = shift

            centroids = new_centroids
            if max_shift <= self.tol:
                break

        self.centroids_ = centroids
        self.labels_ = labels if labels is not None else []
        return self

    def predict(self, X):
        if not hasattr(self, "centroids_"):
            raise ValueError("Model has not been fitted yet")
        self._validate_X(X)
        return self._assign_labels(X, self.centroids_)
