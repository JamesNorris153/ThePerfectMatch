function [all_theta] = oneVsAll(X, y, num_labels, lambda)
%   [all_theta] = ONEVSALL(X, y, num_labels, lambda) trains num_labels
%   logisitc regression classifiers and returns each of these classifiers
%   in a matrix all_theta, where the i-th row of all_theta corresponds 
%   to the classifier for label i

%number of rows in X (number of training examples)
m = size(X, 1);

%number of columns in X (number of features in a training example)
n = size(X, 2);

%theta values
all_theta = zeros(num_labels, n + 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

initial_theta = zeros(n + 1, 1);
options = optimset('GradObj', 'on', 'MaxIter', 500);

for c = 1:num_labels

    %fmincg is used to optimize the cost function.
	[theta] = fmincg (@(t)(lrCostFunction(t, X, (y == c), lambda)), initial_theta, options);
	all_theta(c,:) = theta';

end

