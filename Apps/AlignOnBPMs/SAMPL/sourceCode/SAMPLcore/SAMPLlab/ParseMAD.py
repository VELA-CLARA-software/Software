function [cptlist, svals, evals] = ParseMAD(fname,blname,beam,varargin)

    madfile = fopen(fname);
    
    fgetl(madfile);
    fgetl(madfile);

    % Make a first pass to define parameters
    while ~feof(madfile)
        
        curr = GetNextLine(madfile);
        
        assn = strfind(curr,':=');
        if ~isempty(assn)

            curr = strrep(curr,':','');
            curr = strrep(curr,',',';');
            curr = strrep(curr,'''','prime');

            eval(curr);

        end
    end
    
    frewind(madfile);
    fgetl(madfile);
    fgetl(madfile);
    
    nline = 1;
    linename = {};
    linedefn = {};
    
    brho = beam.rigidity;

    rfsetf = false;
    if nargin>3
        if strcmpi(varargin{1},'frequency')
            rfsetf = true;
        end
    end
    
    % Make a second pass to define components and beam lines
    while ~feof(madfile)

        curr = GetNextLine(madfile);
        lcurr = lower(curr);
        
        name = '';
        ndel = strfind(lcurr,':');
        if ~isempty(ndel)
            name = lcurr(1:(ndel-1));
        end
        
        tilt = 0;
        eval(['tilt =' GetParameter(curr,'TILT') ';']);
        if tilt ~= 0
            fprintf('%s: tilt angle of %6.3f radians ignored\n',name,tilt);
        end

        mrkr = strfind(lcurr,':marker');
        if ~isempty(mrkr)
            name = lcurr(1:(mrkr-1));
            eval([name ' = Marker;']);
            eval([name '.name = ''' name ''';']);
        end
        
        mntr = strfind(lcurr,':monitor');
        if ~isempty(mntr)
            name = lcurr(1:(mntr-1));
            eval([name ' = Drift;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            fprintf('%s: cannot parse MAD8 ''monitor'' - replaced with ''Drift'' \n',name);
        end
        
        hmntr = strfind(lcurr,':hmonitor');
        if ~isempty(hmntr)
            name = lcurr(1:(hmntr-1));
            eval([name ' = Drift;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            fprintf('%s: cannot parse MAD8 ''hmonitor'' - replaced with ''Drift'' \n',name);
        end
        
        vmntr = strfind(lcurr,':vmonitor');
        if ~isempty(vmntr)
            name = lcurr(1:(vmntr-1));
            eval([name ' = Drift;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            fprintf('%s: cannot parse MAD8 ''vmonitor'' - replaced with ''Drift'' \n',name);
        end
        
        instrmnt = strfind(lcurr,':instrument');
        if ~isempty(instrmnt)
            name = lcurr(1:(instrmnt-1));
            eval([name ' = Marker;']);
            eval([name '.name = ''' name ''';']);
            fprintf('%s: cannot parse MAD8 ''instrument'' - replaced with ''Marker'' \n',name);
        end
        
        mltple = strfind(lcurr,':multipole');
        if ~isempty(mltple)
            name = lcurr(1:(mltple-1));
            eval([name ' = Marker;']);
            eval([name '.name = ''' name ''';']);
            fprintf('%s: cannot parse MAD8 ''multipole'' - replaced with ''Marker'' \n',name);
        end
        
        drft = strfind(lcurr,':drift');
        if ~isempty(drft)
            name = lcurr(1:(drft-1));
            eval([name ' = Drift;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
        end
        
        kckr = strfind(lcurr,':kicker');
        if ~isempty(kckr)
            name = lcurr(1:(kckr-1));
            eval([name ' = OrbitCorrector;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval(['len = ' GetParameter(curr,'L') ';']);
            if len>0
                kscale = ['brho/(' GetParameter(curr,'L') ')*'];
                eval([name '.field = [' kscale GetParameter(curr,'VKICK') ',-' kscale GetParameter(curr,'HKICK') '];']);
            end
        end
        
        hkckr = strfind(lcurr,':hkicker');
        if ~isempty(hkckr)
            name = lcurr(1:(hkckr-1));
            eval([name ' = OrbitCorrector;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval(['len = ' GetParameter(curr,'L') ';']);
            if len>0
                kscale = ['brho/(' GetParameter(curr,'L') ')*'];
                eval([name '.field = [0,-' kscale GetParameter(curr,'KICK') '];']);
            end
        end
        
        vkckr = strfind(lcurr,':vkicker');
        if ~isempty(vkckr)
            name = lcurr(1:(vkckr-1));
            eval(['len = ' GetParameter(curr,'L') ';']);
            eval([name ' = OrbitCorrector;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            if len>0
                kscale = ['brho/(' GetParameter(curr,'L') ')*'];
                eval([name '.field = [' kscale GetParameter(curr,'KICK') ',0];']);
            end
        end
        
        rbnd = strfind(lcurr,':rbend');
        if ~isempty(rbnd)
            name = lcurr(1:(rbnd-1));
            eval([name ' = Dipole;']);
            eval([name '.name = ''' name ''';']);
%             eval([name '.length = ' GetParameter(curr,'L') '*(' GetParameter(curr,'ANGLE') '/2)/sin(' GetParameter(curr,'ANGLE') '/2);']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval([name '.angle = ' GetParameter(curr,'ANGLE') ';']);
            eval([name '.field = brho*' GetParameter(curr,'ANGLE') '/' GetParameter(curr,'L') ';']);
            eval([name '.gradient =-brho*' GetParameter(curr,'K1') ';']);
            eval([name '.e1 = ' GetParameter(curr,'E1') '+' GetParameter(curr,'ANGLE') '/2;']);
            eval([name '.e2 = ' GetParameter(curr,'E2') '+' GetParameter(curr,'ANGLE') '/2;']);
            eval([name '.hgap = ' GetParameter(curr,'HGAP') ';']);
            eval([name '.fint1 = ' GetParameter(curr,'FINT') ';']);
            eval([name '.fint2 = ' GetParameter(curr,'FINTX') ';']);
        end
        
        sbnd = strfind(lcurr,':sbend');
        if ~isempty(sbnd)
            name = lcurr(1:(sbnd-1));
            eval([name ' = Dipole;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval([name '.angle = ' GetParameter(curr,'ANGLE') ';']);
            eval([name '.field = brho*' GetParameter(curr,'ANGLE') '/' GetParameter(curr,'L') ';']);
            eval([name '.gradient = brho*' GetParameter(curr,'K1') ';']);
            eval([name '.e1 = ' GetParameter(curr,'E1') ';']);
            eval([name '.e2 = ' GetParameter(curr,'E2') ';']);
            eval([name '.hgap = ' GetParameter(curr,'HGAP') ';']);
            eval([name '.fint1 = ' GetParameter(curr,'FINT') ';']);
            eval([name '.fint2 = ' GetParameter(curr,'FINTX') ';']);
        end
        
        quad = strfind(lcurr,':quadrupole');
        if ~isempty(quad)
            name = lcurr(1:(quad-1));
            k1 = eval(GetParameter(curr,'K1'));
            if k1~=0
                eval([name ' = Quadrupole;']);
                eval([name '.name = ''' name ''';']);
                eval([name '.length = ' GetParameter(curr,'L') ';']);
                eval([name '.gradient = brho*' GetParameter(curr,'K1') ';']);
            else
                eval([name ' = Drift;']);
                eval([name '.name = ''' name ''';']);
                eval([name '.length = ' GetParameter(curr,'L') ';']);
            end
        end
        
        sxt = strfind(lcurr,':sextupole');
        if ~isempty(sxt)
            name = lcurr(1:(sxt-1));
            eval([name ' = Sextupole;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval([name '.gradient = brho*' GetParameter(curr,'K2') ';']);
        end
        
        lcvty = strfind(lcurr,':lcavity');
        if ~isempty(lcvty)
            name = lcurr(1:(lcvty-1));
            eval([name ' = RFAcceleratingStructure;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.structuretype = ''TravellingWave'';']);
            eval([name '.ncell = 1;']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval([name '.voltage = 1e6*' GetParameter(curr,'DELTAE') ';']);
            eval([name '.harmonic = 1;']);
            eval([name '.phase = 2*pi*' GetParameter(curr,'PHI0') ';']);
            eval(['MasterOscillator.SetFrequency(' GetParameter(curr,'FREQ') '*1e6);']);
            rfsetf = true;
%             eval([name '.globalclock = 0;']);
        end
        
        rfcvty = strfind(lcurr,':rfcavity');
        if ~isempty(rfcvty)
            name = lcurr(1:(rfcvty-1));
            eval([name ' = RFCavity;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' GetParameter(curr,'L') ';']);
            eval([name '.voltage = 1e6*' GetParameter(curr,'VOLT') ';']);
            eval([name '.phase = 2*pi*' GetParameter(curr,'LAG') ';']);
            if rfsetf
                eval(['MasterOscillator.SetFrequency(' GetParameter(curr,'FREQ') '*1e6);']);
                eval([name '.harmonic = 1;']);
            else
                eval([name '.harmonic = ' GetParameter(curr,'HARMON') ';']);
            end
        end
        
        bmln = strfind(lcurr,':line=');
        if ~isempty(bmln)
            linename{nline} = lcurr(1:(bmln-1));
%             fprintf([linename{nline} '\n']);
            linedefn{nline} = List2Cell(lcurr((bmln+7):(end-1)));
            nline = nline + 1;
        end
        
    end

    fclose(madfile);
    
    
    % Iteratively expand the required cptlist
    tline = find(strcmpi(blname,linename));
    
    tlinedefn = linedefn{tline(1)};
    makesubs  = 1;
    
    while makesubs
        
        nlinedefn = {};
        makesubs = 0;
    
        for n = 1:size(tlinedefn,2)
            
            tlinedefnn = tlinedefn{n};
            
            isrev = strfind(tlinedefnn,'@');
            if isrev
               tlinedefnn = tlinedefnn(1:end-1);
               revmk = ['''' num2str(int32(rand(1)*1e8)) ''''];
            end
            
            tline1 = find(strcmp(tlinedefnn,linename));
            if ~isempty(tline1)
                if isrev
                    nlinedefn = [nlinedefn revmk linedefn{tline1(1)} revmk];
                else
                    nlinedefn = [nlinedefn linedefn{tline1(1)}];
                end
                makesubs = makesubs + 1;
%                 fprintf([linename{tline1(1)} '\n']);
            else
                nlinedefn = [nlinedefn tlinedefnn];
            end
        end
        
%         fprintf('\n');
        
        tlinedefn = nlinedefn;

    end
    
    cptlist = {};
    revflags = containers.Map();
            
    for n = 1:size(tlinedefn,2)
        
        eval(['cptlist{n} = ' tlinedefn{n} ';']);
        
        if ischar(cptlist{n})
            if isKey(revflags,cptlist{n})
                revflags(cptlist{n}) = [revflags(cptlist{n}) n];
            else
                revflags(cptlist{n}) = n;
            end
        end
        
    end
    
    flgk = revflags.keys;
    for n = 1:(revflags.length)
        
        flgv(n,:) = revflags(flgk{n});
        cptordr = [1:flgv(n,1) (flgv(n,2)-1):-1:(flgv(n,1)+1) flgv(n,2):size(cptlist,2)];
        cptlist = cptlist(cptordr);
        
    end
    
    if revflags.length>0
        cptlist = cptlist(sort(setdiff(1:size(cptlist,2),flgv(1:end))));
    end
    
    if ~rfsetf
        s = 0;
        for n = 1:numel(cptlist)
            s = s + cptlist{n}.length;
        end
        MasterOscillator.SetFrequency(beam.beta*PhysicalConstants.SpeedOfLight/s);
    end
    
    
    s      = 0;
    svals  = zeros(1,numel(cptlist)+1);
    
    evals  = zeros(1,numel(cptlist)+1);
    evals(1) = beam.energy;
    
    pscale = 1;
    ncav   = 0;
    
    logfile = fopen('ParseMAD.log','w');
    fprintf(logfile,'Beam line: %s\n',blname);
    fprintf(logfile,'-------------------------------------------------------------\n');
    fprintf(logfile,'Index  Distance     Energy Class        Name           Length\n');
    fprintf(logfile,'            (m)      (MeV)                                (m)\n');
    fprintf(logfile,'-------------------------------------------------------------\n');
    
    for n = 1:numel(cptlist)

        cpttype = class(cptlist{n});
        fprintf(logfile,'%4i %10.4f %10.4f %-12s %-12s %8.4f\n',...
                         n, ...
                         s, ...
                         beam.energy/PhysicalUnits.MeV, ...
                         cpttype(1:min(numel(cpttype),11)), ...
                         cptlist{n}.name, ...
                         cptlist{n}.length);
        
        if strcmpi(cpttype,'orbitcorrector')
            cptlist{n}.field = pscale * cptlist{n}.field; %#ok<*AGROW>
        end
                     
        if strcmpi(cpttype,'dipole')
            cptlist{n}.field = pscale * cptlist{n}.field;
            cptlist{n}.gradient = pscale * cptlist{n}.gradient;
        end
        
        if strcmpi(cpttype,'quadrupole')
            cptlist{n}.gradient = pscale * cptlist{n}.gradient;
        end
        
        if strcmpi(cpttype,'sextupole')
            cptlist{n}.gradient = pscale * cptlist{n}.gradient;
        end
        
        if strcmpi(cpttype,'rfacceleratingstructure')
            ncav = ncav + 1;
            name = [cptlist{n}.name num2str(ncav)];
            eval([name ' = rfacceleratingstructure;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' num2str(cptlist{n}.length) ';']);
            eval([name '.voltage = ' num2str(sign(beam.species.charge)*cptlist{n}.voltage) ';']);
            eval([name '.harmonic = ' num2str(cptlist{n}.harmonic) ';']);
            p1   = cptlist{n}.frequency*(s + cptlist{n}.length/2)/beam.beta/PhysicalConstants.SpeedOfLight;
            phi0 = cptlist{n}.phase;
            phi1 = phi0 - 2*pi*(p1 - floor(p1));
            eval([name '.phase = ' num2str(phi1) ';']);
            eval(['cptlist{n} = ' name ';']);
            beam.energy = beam.energy + beam.species.charge * cptlist{n}.voltage * cos(phi0);
            pscale = beam.rigidity / brho;
        end
    
        if strcmpi(cpttype,'rfcavity')
            ncav = ncav + 1;
            name = [cptlist{n}.name num2str(ncav)];
            eval([name ' = rfcavity;']);
            eval([name '.name = ''' name ''';']);
            eval([name '.length = ' num2str(cptlist{n}.length) ';']);
            eval([name '.voltage = ' num2str(cptlist{n}.voltage) ';']);
            eval([name '.harmonic = ' num2str(cptlist{n}.harmonic) ';']);
            p1 = cptlist{n}.frequency*(s + cptlist{n}.length/2)/beam.beta/PhysicalConstants.SpeedOfLight;
            phi = cptlist{n}.phase - 2*pi*(p1 - floor(p1));
            eval([name '.phase = ' num2str(phi) ';']);
            eval(['cptlist{n} = ' name ';']);
        end
        
        s = s + cptlist{n}.length;
        svals(n+1) = s;
        evals(n+1) = beam.energy;
        
    end
    
    fclose(logfile);
    
    
return


function nextline = GetNextLine(fid)

    nextline = fgetl(fid);
    cont = strfind(nextline,'&');        
    while ~isempty(cont)
        nextline1 = fgetl(fid);
        nextline = [nextline(1:(end-1)) nextline1];
        cont = strfind(nextline,'&');
    end

    cmnt = strfind(nextline,'!');
    if ~isempty(cmnt)
        nextline = nextline(1:(cmnt(1)-1));
    end
    
    nextline = strrep(nextline,' ','');
    nextline = [nextline ','];

return
    
    
function param = GetParameter(strng, name)

    ppos1 = strfind(lower(strng),[lower(name) '=']);
    param = '0';
    if ~isempty(ppos1)
        strng = strng((ppos1+1+size(name,2)):end);
        ppos1 = strfind(strng,',');
        param = strng(1:(ppos1-1));
    end
    
return


function cellarray = List2Cell(list)

    cellarray = {};
    nitems = 1;
    
    term = [ strfind(list,',') strfind(list,')') ];
    
    while ~isempty(term)
        
        lstitem = list(1:(term(1)-1));
        
        isrev = strfind(lstitem,'-');
        if ~isempty(isrev)
            lstitem = [lstitem((isrev+1):end) '@'];
        end
        
        mltpl = 1;
        ismlt = strfind(lstitem,'*');
        if ~isempty(ismlt)
            mltpl = eval(lstitem(1:(ismlt-1)));
            lstitem = lstitem((ismlt+1):end);
        end
        
        for n = 0:(mltpl-1)
            cellarray{nitems+n} = lstitem;
        end
        nitems = nitems + mltpl;
        
        list = list((term(1)+1):end);
        term = [ strfind(list,',') strfind(list,')') ];
        
%         fprintf(['  ' cellarray{nitems} '\n']);
        
    end

return