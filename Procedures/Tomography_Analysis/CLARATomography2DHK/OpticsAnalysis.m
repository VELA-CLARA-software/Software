clear

dirname    = 'Data 2019-03-04';
configfile = 'ImageFileInformation.mat';

load([dirname '/' configfile]);

% Select a subset of the data

indx1         = find(QuadCurrents(:,3)>0);
indx2         = find(QuadCurrents(:,3)<0);

indx          = 1:size(QuadCurrents,1);

Image_and_background_filenames_at_observation_point = Image_and_background_filenames_at_observation_point(indx,:);

QuadCurrents = QuadCurrents(indx,:);

% betax        = 26.00;
% alphax       =  2.40;
% betay        =  9.00;
% alphay       =  1.80;

betax        = Beta_x_y_at_reconstruction_point(1);
alphax       = Alpha_x_y_at_reconstruction_point(1);
betay        = Beta_x_y_at_reconstruction_point(2);
alphay       = Alpha_x_y_at_reconstruction_point(2);

optics       = CalculateOptics(betax, alphax, betay, alphay, QuadCurrents);

figure(2)
plot(optics(indx1,5),optics(indx1,6),'.b');
hold on
plot(optics(indx2,5),optics(indx2,6),'.r');
axis([0 pi 0 pi])
xlabel('horizontal phase advance (rad)')
ylabel('vertical phase advance (rad)')
legend('Q3 current > 0','Q3 current < 0')

set(gcf,'PaperUnits','inches')
set(gcf,'PaperPosition',[1 5 6 6])
% print('-dpng','PhaseAdvances.png','-r600')
print('-dpdf','PhaseAdvances.pdf')
