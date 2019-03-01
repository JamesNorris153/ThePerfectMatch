function [score2] = main(X, y, m, X2)
    %% Setup the parameters
    num_labels = 2;          % 2 labels indicate the result can be either 0 or 1 

    X = double(cell2mat(X));
    y = double(cell2mat(y));
    X = reshape(X, [m, size(X, 2) / m]);

    y = reshape(y, [m, 1]);
    %m = size(X, 1);

    %% Apply linear regression
    lambda = 0.5;
    [all_theta] = oneVsAll(X, y, num_labels, lambda);

    %% Prediction
    X2 = double(cell2mat(X2));
    X2 = reshape(X2, [m, size(X2, 2) / m]);
    score2 = predictOneVsAll(all_theta, X2);
    pred2 = round(score2);

end
