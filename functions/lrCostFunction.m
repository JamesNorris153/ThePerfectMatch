function [J, grad] = lrCostFunction(theta, X, y, lambda)

%   J = LRCOSTFUNCTION(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

m = length(y); % number of training examples

J = 0;
grad = zeros(size(theta));

tempTheta = theta;
tempTheta(1) = 0;

J = (-1 / m) * sum(y.*log(sigmoid(X * theta)) + (1 - y).*log(1 - sigmoid(X * theta))) + (lambda / (2 * m))*sum(tempTheta.^2);
temp = sigmoid (X * theta);
error = temp - y;
grad = (1 / m) * (X' * error) + (lambda/m)*tempTheta;

end
