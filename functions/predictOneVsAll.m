function p = predictOneVsAll(all_theta, X)

%  p = PREDICTONEVSALL(all_theta, X) will return a vector of predictions
%  for each example in the matrix X. 

m = size(X, 1);

p = zeros(size(X, 1), 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

indices = max(sigmoid(all_theta * X'));

p = indices';

end
