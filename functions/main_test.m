function [score2] = main_test(X, y, m, X2, y2, m2)
    %% Setup the parameters
    num_labels = 2;          % 2 labels indicate the result can be either 0 or 1 
    X = double(cell2mat(X));
    y = double(cell2mat(y));
    X = reshape(X, [m, size(X, 2) / m]);

    y = reshape(y, [m, 1]);

    %% Apply linear regression
    lambda = 0.5;
    [all_theta] = oneVsAll(X, y, num_labels, lambda);

    %% Compare results
    X2 = double(cell2mat(X2));
    X2 = reshape(X2, [m2, size(X2, 2) / m2]);
    y2 = double(cell2mat(y2));
    y2 = reshape(y2, [m2,1]);
    score2 = predictOneVsAll(all_theta, X2);
    pred2 = round(score2);

    fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred2 == y2)) * 100);
end
