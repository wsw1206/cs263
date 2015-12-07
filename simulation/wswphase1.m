data = csvread('wswphase1.csv', 1, 0);
%data = data(1:1000,:);
amount = data(:,2);
m = min(amount);
amount = amount-m;
% data = data(1000:2000,:);
%data = data(2000:3000,:);
% data = data(3000:4000,:);
figure
hold on
plot (data(:,1), data(:,2), 'r')
plot (data(:,1), data(:,3), 'b')
x = 1:1000;
%plot (x, 10*sin(x/150)+30, 'g')
x=[0.28 0.28];
y=[0.5 0.55];
annotation('arrow',x,y)