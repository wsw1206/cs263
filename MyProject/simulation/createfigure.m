function createfigure(X1, YMatrix1)
%CREATEFIGURE(X1, YMATRIX1)
%  X1:  vector of x data
%  YMATRIX1:  matrix of y data

%  Auto-generated by MATLAB on 18-Dec-2014 14:43:01

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'all');

% Create multiple lines using matrix input to plot
plot1 = plot(X1,YMatrix1,'Parent',axes1);
set(plot1(1),'Color',[1 0 0]);
set(plot1(2),'Color',[0 0 1]);
set(plot1(3),'Color',[1 0 0]);
set(plot1(4),'Color',[0 0 1]);

% Create legend
legend1 = legend(axes1,'show');
size(legend1)
set(legend1,...
    'Position',[0.742204784052542 0.619799031872077 0.105514269482844 0.106049439791145]);

% Create line
annotation(figure1,'line',[0.285505124450952 0.284040995607613],...
    [0.116241379310345 0.920689655172414],'LineStyle',':');

% Create arrow
annotation(figure1,'arrow',[0.330893118594436 0.28696925329429],...
    [0.605896551724138 0.567241379310345]);

% Create textbox
annotation(figure1,'textbox',...
    [0.277777870738339 0.570235934664246 0.123393432336331 0.0690476190476203],...
    'String',{'Snakes Added'},...
    'FitBoxToText','off',...
    'EdgeColor',[1 1 1]);

