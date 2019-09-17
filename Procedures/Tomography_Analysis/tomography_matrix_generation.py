#
# Build the Tomography Matrix ,
# we're going to try adn reproduce this code from the matlab script
"""
for n = 1:nx

    indx   = indxx(n);

    % Set the phase advance

    cosmux = cos(PhaseAdvance_x_y(indx,1));
    sinmux = sin(PhaseAdvance_x_y(indx,1));

    % Find the indices of the non-zero values of the matrix relating the
    % projected distribution at YAG02 to the phase space distribution at YAG01

    for xindx1 = 1:psresn
        for pxindx1 = 1:psresn
            xindx0  = round(cosmux*(xindx1 - ctroffset) - sinmux*(pxindx1 - ctroffset) + ctroffset);
            if xindx0>0 && xindx0<=psresn
                pxindx0 = round(sinmux*(xindx1 - ctroffset) + cosmux*(pxindx1 - ctroffset) + ctroffset);
                if pxindx0>0 && pxindx0<=psresn

                    dfindxx(:,dfcntrx) = [(n-1)*psresn + xindx1; (xindx0-1)*psresn + pxindx0];
                    dfcntrx = dfcntrx + 1;

                end
            end
        end
    end

    % Construct the vector of image pixels
    % why not normalised?
%     nrm = sum(sum(imagearray{indx}));

    xprojection(((n-1)*psresn+1):n*psresn) = sum(imagearray{indx},2); %/nrm;

end
"""




