function [score2] = main(X, y, m, X2, y2)
%% Initialization
    
    %% Setup the parameters
    num_labels = 2;          % 2 labels indicate the result can be either 0 or 1 

    %data = load('score.txt');
    %X = data(:, 1:end - 1);
    %y = data(:, end);
    X = double(cell2mat(X));
    y = double(cell2mat(y));
    X = reshape(X, [m, size(X, 2) / m]);

    y = reshape(y, [m, 1]);
    %m = size(X, 1);

    %% Apply linear regression
    lambda = 0.5;
    [all_theta] = oneVsAll(X, y, num_labels, lambda);

    %% Prediction
    score = predictOneVsAll(all_theta, X);

    pred = round(score);
    %fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

    %% Write to txt file
    %fid = fopen('result.txt', 'wt');
    
    %data2 = load('score2.txt');
    %X2 = data2(:, 1:end - 1);
    %y2 = data2(:, end);
    X2 = double(cell2mat(X2));
    X2 = reshape(X2, [m, size(X2, 2) / m]);
    y2 = double(cell2mat(y2));
    y2 = reshape(y2, [m,1]);
    score2 = predictOneVsAll(all_theta, X2);
    pred2 = round(score2);






    fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred2 == y2)) * 100);
end
