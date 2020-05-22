SDDS1
!# little-endian
&description text="sigma matrix--input: S02.ele  lattice: S02.lte", contents="sigma matrix", &end
&parameter name=Step, description="Simulation step", type=long, &end
&parameter name=SVNVersion, description="SVN version number", type=string, fixed_value=26112M, &end
&column name=s, units=m, description=Distance, type=double,  &end
&column name=ElementName, description="Element name", format_string=%10s, type=string,  &end
&column name=ElementOccurence, description="Occurence of element", format_string=%6ld, type=long,  &end
&column name=ElementType, description="Element-type name", format_string=%10s, type=string,  &end
&column name=s1, symbol="$gs$r$b1$n", units=m, description="sqrt(<x*x>)", type=double,  &end
&column name=s12, symbol="$gs$r$b12$n", units=m, description="<x*xp'>", type=double,  &end
&column name=s13, symbol="$gs$r$b13$n", units="m$a2$n", description="<x*y>", type=double,  &end
&column name=s14, symbol="$gs$r$b14$n", units=m, description="<x*y'>", type=double,  &end
&column name=s15, symbol="$gs$r$b15$n", units="m$a2$n", description="<x*s>", type=double,  &end
&column name=s16, symbol="$gs$r$b16$n", units=m, description="<x*delta>", type=double,  &end
&column name=s17, symbol="$gs$r$b17$n", units="m*s", description="<x*t>", type=double,  &end
&column name=s2, symbol="$gs$r$b2$n", description="sqrt(<x'*x'>)", type=double,  &end
&column name=s23, symbol="$gs$r$b23$n", units=m, description="<x'*y>", type=double,  &end
&column name=s24, symbol="$gs$r$b24$n", description="<x'*y'>", type=double,  &end
&column name=s25, symbol="$gs$r$b25$n", units=m, description="<x'*s>", type=double,  &end
&column name=s26, symbol="$gs$r$b26$n", description="<x'*delta>", type=double,  &end
&column name=s27, symbol="$gs$r$b27$n", units=s, description="<x'*t>", type=double,  &end
&column name=s3, symbol="$gs$r$b3$n", units=m, description="sqrt(<y*y>)", type=double,  &end
&column name=s34, symbol="$gs$r$b34$n", units=m, description="<y*y'>", type=double,  &end
&column name=s35, symbol="$gs$r$b35$n", units="m$a2$n", description="<y*s>", type=double,  &end
&column name=s36, symbol="$gs$r$b36$n", units=m, description="<y*delta>", type=double,  &end
&column name=s37, symbol="$gs$r$b37$n", units="m*s", description="<y*t>", type=double,  &end
&column name=s4, symbol="$gs$r$b4$n", description="sqrt(<y'*y')>", type=double,  &end
&column name=s45, symbol="$gs$r$b45$n", units=m, description="<y'*s>", type=double,  &end
&column name=s46, symbol="$gs$r$b46$n", description="<y'*delta>", type=double,  &end
&column name=s47, symbol="$gs$r$b47$n", units=s, description="<y'*t>", type=double,  &end
&column name=s5, symbol="$gs$r$b5$n", units=m, description="sqrt(<s*s>)", type=double,  &end
&column name=s56, symbol="$gs$r$b56$n", units=m, description="<s*delta>", type=double,  &end
&column name=s57, symbol="$gs$r$b57$n", units="m*s", description="<s*t>", type=double,  &end
&column name=s6, symbol="$gs$r$b6$n", description="sqrt(<delta*delta>)", type=double,  &end
&column name=s67, symbol="$gs$r$b67$n", units=s, description="<delta*t>", type=double,  &end
&column name=s7, symbol="$gs$r$b7$n", description="sqrt(<t*t>)", type=double,  &end
&column name=ma1, symbol="max$sb$ex$sb$e", units=m, description="maximum absolute value of x", type=double,  &end
&column name=ma2, symbol="max$sb$ex'$sb$e", description="maximum absolute value of x'", type=double,  &end
&column name=ma3, symbol="max$sb$ey$sb$e", units=m, description="maximum absolute value of y", type=double,  &end
&column name=ma4, symbol="max$sb$ey'$sb$e", description="maximum absolute value of y'", type=double,  &end
&column name=ma5, symbol="max$sb$e$gD$rs$sb$e", units=m, description="maximum absolute deviation of s", type=double,  &end
&column name=ma6, symbol="max$sb$e$gd$r$sb$e", description="maximum absolute value of delta", type=double,  &end
&column name=ma7, symbol="max$sb$e$gD$rt$sb$e", units=s, description="maximum absolute deviation of t", type=double,  &end
&column name=minimum1, symbol="x$bmin$n", units=m, type=double,  &end
&column name=minimum2, symbol="x'$bmin$n", units=m, type=double,  &end
&column name=minimum3, symbol="y$bmin$n", units=m, type=double,  &end
&column name=minimum4, symbol="y'$bmin$n", units=m, type=double,  &end
&column name=minimum5, symbol="$gD$rs$bmin$n", units=m, type=double,  &end
&column name=minimum6, symbol="$gd$r$bmin$n", units=m, type=double,  &end
&column name=minimum7, symbol="t$bmin$n", units=s, type=double,  &end
&column name=maximum1, symbol="x$bmax$n", units=m, type=double,  &end
&column name=maximum2, symbol="x'$bmax$n", units=m, type=double,  &end
&column name=maximum3, symbol="y$bmax$n", units=m, type=double,  &end
&column name=maximum4, symbol="y'$bmax$n", units=m, type=double,  &end
&column name=maximum5, symbol="$gD$rs$bmax$n", units=m, type=double,  &end
&column name=maximum6, symbol="$gd$r$bmax$n", units=m, type=double,  &end
&column name=maximum7, symbol="t$bmax$n", units=s, type=double,  &end
&column name=Sx, symbol="$gs$r$bx$n", units=m, description=sqrt(<(x-<x>)^2>), type=double,  &end
&column name=Sxp, symbol="$gs$r$bx'$n", description=sqrt(<(x'-<x'>)^2>), type=double,  &end
&column name=Sy, symbol="$gs$r$by$n", units=m, description=sqrt(<(y-<y>)^2>), type=double,  &end
&column name=Syp, symbol="$gs$r$by'$n", description=sqrt(<(y'-<y'>)^2>), type=double,  &end
&column name=Ss, symbol="$gs$r$bs$n", units=m, description=sqrt(<(s-<s>)^2>), type=double,  &end
&column name=Sdelta, symbol="$gs$bd$n$r", description=sqrt(<(delta-<delta>)^2>), type=double,  &end
&column name=St, symbol="$gs$r$bt$n", units=s, description=sqrt(<(t-<t>)^2>), type=double,  &end
&column name=ex, symbol="$ge$r$bx$n", units=m, description="geometric horizontal emittance", type=double,  &end
&column name=enx, symbol="$ge$r$bx,n$n", units=m, description="normalized horizontal emittance", type=double,  &end
&column name=ecx, symbol="$ge$r$bx,c$n", units=m, description="geometric horizontal emittance less dispersive contributions", type=double,  &end
&column name=ecnx, symbol="$ge$r$bx,cn$n", units=m, description="normalized horizontal emittance less dispersive contributions", type=double,  &end
&column name=ey, symbol="$ge$r$by$n", units=m, description="geometric vertical emittance", type=double,  &end
&column name=eny, symbol="$ge$r$by,n$n", units=m, description="normalized vertical emittance", type=double,  &end
&column name=ecy, symbol="$ge$r$by,c$n", units=m, description="geometric vertical emittance less dispersive contributions", type=double,  &end
&column name=ecny, symbol="$ge$r$by,cn$n", units=m, description="normalized vertical emittance less dispersive contributions", type=double,  &end
&column name=betaxBeam, symbol="$gb$r$bx,beam$n", units=m, description="betax for the beam, excluding dispersive contributions", type=double,  &end
&column name=alphaxBeam, symbol="$ga$r$bx,beam$n", description="alphax for the beam, excluding dispersive contributions", type=double,  &end
&column name=betayBeam, symbol="$gb$r$by,beam$n", units=m, description="betay for the beam, excluding dispersive contributions", type=double,  &end
&column name=alphayBeam, symbol="$ga$r$by,beam$n", description="alphay for the beam, excluding dispersive contributions", type=double,  &end
&data mode=binary, &end
                 _BEG_      MARK�]�Nr=`?�;�Lj�����ηѕ���T�s�P6��m�q>^���x�����%c�<Ԏf��/?]c���,J>�b\(?sL>��*���=���A�OS>����z�9�!�X1`?�Z�3pL��˔:_2�d>CJ?�Ș�����=��<�0�/?��Bt�xU�IX�L:�>u ��:��2�׻c�P?}i�V�ܾ}~��<%��U|?]�#�\�����э=p����m?[z���A?/a�A��p?Tv�I�A?�J~��e?Wa�ة��?�Z؇��=p����m�4�lA�/a�A��p�Tv�I�A�T*O���R�Wa�ة���-\�����y�k?[z���A?t�gK"�l?����@?�J~��e?{#A>�x?�Z؇��=�]�Nr=`?Ԏf��/?9�!�X1`?�0�/?2�׻c�P?%��U|?���э=�adCͺ�>H'TL\�>�MC�붊>DV�X�>d�A�Kō>ه�Y�>/v�ѭu�>���-�>�#d��3@fk`��@1n��1@x������?           START      CHARGE�]�Nr=`?�;�Lj�����ηѕ���T�s�P6��m�q>^���x�����%c�<Ԏf��/?]c���,J>�b\(?sL>��*���=���A�OS>����z�9�!�X1`?�Z�3pL��˔:_2�d>CJ?�Ș�����=��<�0�/?��Bt�xU�IX�L:�>u ��:��2�׻c�P?}i�V�ܾ}~��<%��U|?]�#�\�����э=p����m?[z���A?/a�A��p?Tv�I�A?�J~��e?Wa�ة��?�Z؇��=p����m�4�lA�/a�A��p�Tv�I�A�T*O���R�Wa�ة���-\�����y�k?[z���A?t�gK"�l?����@?�J~��e?{#A>�x?�Z؇��=�]�Nr=`?Ԏf��/?9�!�X1`?�0�/?2�׻c�P?%��U|?���э=�adCͺ�>H'TL\�>�MC�붊>DV�X�>d�A�Kō>ه�Y�>/v�ѭu�>���-�>�#d��3@fk`��@1n��1@x������?           CLA-S02-APER-01      RCOL�]�Nr=`?�;�Lj�����ηѕ���T�s�P6��m�q>^���x�����%c�<Ԏf��/?]c���,J>�b\(?sL>��*���=���A�OS>����z�9�!�X1`?�Z�3pL��˔:_2�d>CJ?�Ș�����=��<�0�/?��Bt�xU�IX�L:�>u ��:��2�׻c�P?}i�V�ܾ}~��<%��U|?]�#�\�����э=p����m?[z���A?/a�A��p?Tv�I�A?�J~��e?Wa�ة��?�Z؇��=p����m�4�lA�/a�A��p�Tv�I�A�T*O���R�Wa�ة���-\�����y�k?[z���A?t�gK"�l?����@?�J~��e?{#A>�x?�Z؇��=�]�Nr=`?Ԏf��/?9�!�X1`?�0�/?2�׻c�P?%��U|?���э=�adCͺ�>H'TL\�>�MC�붊>DV�X�>d�A�Kō>ه�Y�>/v�ѭu�>���-�>�#d��3@fk`��@1n��1@x������?9	�/���?   CLA-S02-MAG-HVCOR-01      KICKER��zd�`?Cѓ+D���-si ��w�}b�Rs���0bq>�'j�󔾆�8k�"�<Ԏf��/?���o�ZL>�b\(?sL>A���=���A�OS>.8o2=�z�h�`?Pv�[�������	��c>�.���d��
Sϡ<�0�/?��%�xU�IX�L:�>R�E;��a(�f�P?Z�&�Y�ܾR9P���<%��U|?���>#{ͽҍ=E���C�l?[z���A?%����p?Tv�I�A? �Ô��e?Wa�ة��? 
cc0��=E���C�l�4�lA�%����p�Tv�I�A�@�����R�Wa�ة���@�%#�@��w�j?[z���A?�7���l?����@? �Ô��e?{#A>�x? 
cc0��=��zd�`?Ԏf��/?h�`?�0�/?a(�f�P?%��U|?>#{ͽҍ=�adCͺ�>H'TL\�>�MC�붊><V�X�>l�A�Kō>އ�Y�>7v�ѭu�>���-�>�Ar�e3@O��^ �@ۇ̺�~1@ז�F*U�?9-��a�?   DRIFT1      CSRDRIFT7k��`?.3��5���6Z�</���ׂZ-Es�1%�8[q>�6�L@P��Ev�<Ԏf��/?�uį/�L>�b\(?sL>:�c���=���A�OS>،��L�z���.�`?��PD��̅y�c>Ab�Fݗ��ޏ�/��<�0�/?"8���xU�IX�L:�>k.��6;���t��f�P?ly�1Z�ܾ���f	�<%��U|?ڭ��=���I#�ҍ=�����l?[z���A?ҿ͒��p?Tv�I�A?�)�g��e?Wa�ة��?�P��P��=�����l�4�lA�ҿ͒��p�Tv�I�A� � �R�Wa�ة����7�k5򐽹�~�e�j?[z���A?�E�l�l?����@?�)�g��e?{#A>�x?�P��P��=7k��`?Ԏf��/?��.�`?�0�/?�t��f�P?%��U|?�I#�ҍ=�adCͺ�>H'TL\�>�MC�붊>DV�X�>f�A�Kō>ۇ�Y�>1v�ѭu�>���-�>��A�1U3@(����|@kpF�p1@�_^�RE�?��R{�)�?   CLA-S02-MAG-QUAD-01      KQUADK@��=\?��ݨپ����m��٧@
J��D�Xn>�ɧTp�����^�-�<��V�+Em?��x�>�]se�+�>��~��y���8��k�>��H@1���5�n-�a?�?�\f��>��e�[�d>_�n��ݺ,�:�<�-����k?�@H�Azj>I+�q��u(2���<�@ #�P?$>Ǌ�ܾx1{<+	�<]Q��U|?���j�����,�Ӎ=a�_Gi?k>����y?��k���r?�߭]wm}?������e?W��ة��?�Ƃ拇�=a�_Gi���,5�x���k���r��߭]wm}� !  9�R�W��ة��� l��������qg?k>����y?|G�/�o?�~�]Ry?������e?��4A>�x?�Ƃ拇�=K@��=\?��V�+Em?�5�n-�a?�-����k?�@ #�P?]Q��U|?��,�Ӎ=n�f�Eݍ>pNv2�f�><�"�؍>]%~�Kd�>q�j�>�n���n�>gl�8��>��Y/4�>�譂Jc*@�h$Q;@8�j=U8@����&C���J6�?   DRIFT2      CSRDRIFTv�Ry"[?�)�)g�ؾ1nȉY����jȱ����~�'Vm>mdrTّ�q�|�F�<��V�+Em?����n��>�]se�+�>�&�z���8��k�>�Ã�~1���M1�< b?�؏O��>�%L
e>������#h?��٢<�-����k?��޲nj>I+�q���*��Ү�<�����P?mI�J<�ܾq��\��<]Q��U|?gm������WZ�Ӎ=# �,krh?k>����y?�|Xs?�߭]wm}?��0{�e?W��ة��?�3d\\��=# �,krh���,5�x��|Xs��߭]wm}� ��
�R�W��ة����4_>�����n�ϫf?k>����y?Ef���Bp?�~�]Ry?��0{�e?��4A>�x?�3d\\��=v�Ry"[?��V�+Em?�M1�< b?�-����k?�����P?]Q��U|?�WZ�Ӎ=n�f�Eݍ>pNv2�f�>;�"�؍>]%~�Kd�>c�j�>�s���n�>�kl�8��>�
�Y/4�>�pb�(@���W!�:@�0m,�9@;dS�s�C�h�"�?   CLA-S02-DIA-BPM-01      MONI��z�l|X?c4}i�`־+��^3畾?��
ѡ�qJ�Y�|j>7��C.���V�󟹧<��V�+Em?]䄭��>�]se�+�>����sz���8��k�>��Y�.2���rK�bc?��La0��>�?� �%f>�/��n����X�Pأ<�-����k?�|�Nj>I+�q��Y�<*��<���3��P?��O^�ܾ�8^y��<]Q��U|?S0�D����8EWӍ=�ʚY!f?k>����y?9�?�uet?�߭]wm}?�Ǌ+u�e?W��ة��? ���Ն�=�ʚY!f���,5�x�9�?�uet��߭]wm}� g�OY�R�W��ة��� �qt������ﭴ|d?k>����y?7�nFhq?�~�]Ry?�Ǌ+u�e?��4A>�x? ���Ն�=��z�l|X?��V�+Em?�rK�bc?�-����k?���3��P?]Q��U|?��8EWӍ=��f�Eݍ>�Pv2�f�>��"�؍>�'~�Kd�>��j�>�v���n�>|nl�8��>��Y/4�>����$@������7@1���;A=@D7l�$ E�h�>�a��?   DRIFT3      CSRDRIFT�/ko�PH?vDh4�)ƾ��G���$L������u ��hZ>���р�i��E��<��V�+Em?IC��d��>�]se�+�>�|��u|���8��k�>� T�c5���O���Ai?qT6��>kM�>x'k>�1qm�v��:���W�<�-����k?�ۙo��i>I+�q���:kڤ�<]�ģP?Wv;T�ܾ�g>;��<]Q��U|?������!Z��bҍ=��I�!�V?k>����y?���-��z?�߭]wm}? 2Dְ�e?W��ة��? D}c��=��I�!�V���,5�x����-��z��߭]wm}� �Q��R�W��ة��� U�}��M}}�T?k>����y?��f˿v?�~�]Ry? 2Dְ�e?��4A>�x? D}c��=�/ko�PH?��V�+Em?�O���Ai?�-����k?]�ģP?]Q��U|?!Z��bҍ=��f�Eݍ>�Ov2�f�>_�"�؍>�&~�Kd�>��j�>�v���n�>|nl�8��>��Y/4�>2�A0y�@���'@%+�Ǟ�H@^˿H^]K���G���?   CLA-S02-MAG-QUAD-02      KQUADν<AAI7?qZN_�O��$�������0c����p>}u/nXI>�)e;��q��rF#%��<=N&��f?Z�h�"��>
P�M~�����B¡w���	��>�+�},��]8!̎j?�$�;�eؾ e�'k>DeGᴽ��)*�K?Y�<�(�l�]?l�ф^Yf�p�2[P�>��.�	����(�_�P?l�I�ܾ��k��< 5��U|?`ч����)�Ӎ=���}�G?��S �Ms?w�<{?f0a��/o? i� ;�e?ض�ة��? ��2-��=���}�G�s���.�q�w�<{����p�Uj� ��n�R�ض�ة��� 6�+���A�D?��S �Ms?7>��w?f0a��/o? i� ;�e?x�4A>�x? ��2-��=ν<AAI7?=N&��f?]8!̎j?�(�l�]?��(�_�P? 5��U|?�)�Ӎ=��:a���>UL�G�>om8䟍>��*E�>�F���f�>Z~���>n]x-�>�AJQ��>6��;_J�?����@�;Q��C@y���6@������?   DRIFT4      CSRDRIFT�(ƛ?��K_13���/P)Sm����rF�`>{-�y�K*>�:U�0]���Y_c�g<=N&��f?��
��>
P�M~��}��w���	��>�m	/��x"GV�h?�픒6׾�O�ӑ�h>]�o ]o��@W�9
A�<�(�l�]?Zm*6Ff�p�2[P�>J�h?����� �%0�P?�K���ܾnFR��< 5��U|?6̶EX��TpVƶӍ=��uq�0?��S �Ms?߅?��y?f0a��/o? � OJ�e?ض�ة��? �<1��=��uq�0�s���.�q�߅?��y����p�Uj� <���S�ض�ة��� �Nc���-�(�D,?��S �Ms?��D��9v?f0a��/o? � OJ�e?x�4A>�x? �<1��=�(ƛ?=N&��f?x"GV�h?�(�l�]?� �%0�P? 5��U|?TpVƶӍ=��:a���>VL�G�>pm8䟍>��*E�>�G���f�>]���>�n]x-�>�AJQ��>�϶|��?�m�ոm�?���
�A@�?�Vmi5@������?   CLA-S02-DIA-SCR-01-W      WATCH�(ƛ?��K_13���/P)Sm����rF�`>{-�y�K*>�:U�0]���Y_c�g<=N&��f?��
��>
P�M~��}��w���	��>�m	/��x"GV�h?�픒6׾�O�ӑ�h>]�o ]o��@W�9
A�<�(�l�]?Zm*6Ff�p�2[P�>J�h?����� �%0�P?�K���ܾnFR��< 5��U|?6̶EX��TpVƶӍ=��uq�0?��S �Ms?߅?��y?f0a��/o? � OJ�e?ض�ة��? �<1��=��uq�0�s���.�q�߅?��y����p�Uj� <���S�ض�ة��� �Nc���-�(�D,?��S �Ms?��D��9v?f0a��/o? � OJ�e?x�4A>�x? �<1��=�(ƛ?=N&��f?x"GV�h?�(�l�]?� �%0�P? 5��U|?TpVƶӍ=��:a���>VL�G�>pm8䟍>��*E�>�G���f�>]���>�n]x-�>�AJQ��>�϶|��?�m�ոm�?���
�A@�?�Vmi5@h�^-��?   DRIFT5      CSRDRIFTWZ!��5?���W.�>T��h�zi>1��'_=Q�@��9c{E�Sy;6�`>����)?��=N&��f?#��h;�>
P�M~��u�Zօ�w���	��>����2��R�n6�bf?���(�Ծ�v��kWe>	�.�-����rJ&�<�(�l�]??ׇ�)f�p�2[P�>y��
�᣼O�σ�P?z�t���ܾ}��]��< 5��U|?{-\&����_��ԍ=��*cɉF?��S �Ms?�-�w?f0a��/o? �����e?ض�ة��? �2�6��=�ٻ�m�E�s���.�q��-�w����p�Uj� ���S�ض�ة��� �R%����*cɉF?��S �Ms?����EFt?f0a��/o? �����e?x�4A>�x? �2�6��=WZ!��5?=N&��f?R�n6�bf?�(�l�]?O�σ�P? 5��U|?�_��ԍ=��:a���>UL�G�>om8䟍>��*E�>
G���f�>�~���>~n]x-�>AJQ��>�u8��?��e���77f�(=@�kMSz3@^�����?   CLA-S02-MAG-HVCOR-02      KICKER'*��s�:?���&�A�>�sl;�q>���W�[�l��^�)K�7���;g>��z��V��=N&��f?K#c����>
P�M~���6,�8�w���	��>�ᑛ3��u|����e?��Ya{�Ծ��V㶤d>�t�.���pYmR��<�(�l�]?:u��#f�p�2[P�>\����ܣ��g�AۢP?�����ܾ	�ۡ�< 5��U|?�sP����(��ԍ=� �i�J?��S �Ms?����j+w?f0a��/o? g���e?ض�ة��? a��7��=s�!ϤI�s���.�q�����j+w����p�Uj� `ߞS�ض�ة��� �7����� �i�J?��S �Ms??�+�&�s?f0a��/o? g���e?x�4A>�x? a��7��='*��s�:?=N&��f?u|����e?�(�l�]?�g�AۢP? 5��U|?��(��ԍ=��:a���>UL�G�>om8䟍>��*E�>
G���f�>�~���>~n]x-�>AJQ��>b��5ʈ�?���I˶��oI��;@���!!3@��B���?   DRIFT6      CSRDRIFT���D?�݄7}�>K�y�x�}>-s�n��j��#�.�T�;��ϡs>h;������=N&��f?������>
P�M~�������w���	��>_ ��5�������d?���9RrӾi��5�b>�ێ�01��a�����<�(�l�]?]	QK;f�p�2[P�>�v�[У�ձ�g��P?h�)@�ܾ�:,���< 5��U|?�y�p��s��Ս=���}�	S?��S �Ms?�y.+��u?f0a��/o? &ݣ��e?ض�ة��? T��:��=�x�ʼQ�s���.�q��y.+��u����p�Uj� ��NS�ض�ة��� rY˽�����}�	S?��S �Ms?y��7}�r?f0a��/o? &ݣ��e?x�4A>�x? T��:��=���D?=N&��f?�����d?�(�l�]?ձ�g��P? 5��U|?s��Ս=��:a���>UL�G�>om8䟍>��*E�>
G���f�>�~���>~n]x-�>AJQ��>�2��1�?�UJ ������/�09@�xZt�2@h�:{�'�?   CLA-S02-COL-01      ECOL�f�'\uY?q��۫��>���9S�>ȋ됼��X����j��.��b�>k����.��=N&��f?��'(�>
P�M~��iW��!�w���	��>MM�>��Ow6��&_?�sX�;;����X�U>3�֬�����)?p��<�(�l�]?��.C��e�p�2[P�>,Lkl���,2T�P??D�;�ܾ�/��V�< 5��U|?@�/�����2��	؍=��
<�ff?��S �Ms?���e��p?f0a��/o? Ze���e?ض�ة��? *r0H��=h��,'ad�s���.�q����e��p����p�Uj� 0��S�ض�ة��� ��$Z����
<�ff?��S �Ms?�'wnq�l?f0a��/o? Ze���e?x�4A>�x? *r0H��=�f�'\uY?=N&��f?Ow6��&_?�(�l�]?,2T�P? 5��U|?�2��	؍=+�:a���>^L�G�>�k8䟍>'��*E�>�F���f�>Z~���>n]x-�>�AJQ��>Bɥ�%@�Q�4�2��Q��C<,@����+@h�:{�'�?   CLA-S02-APER-02      RCOL�f�'\uY?q��۫��>���9S�>ȋ됼��X����j��.��b�>k����.��=N&��f?��'(�>
P�M~��iW��!�w���	��>MM�>��Ow6��&_?�sX�;;����X�U>3�֬�����)?p��<�(�l�]?��.C��e�p�2[P�>,Lkl���,2T�P??D�;�ܾ�/��V�< 5��U|?@�/�����2��	؍=��
<�ff?��S �Ms?���e��p?f0a��/o? Ze���e?ض�ة��? *r0H��=h��,'ad�s���.�q����e��p����p�Uj� 0��S�ض�ة��� ��$Z����
<�ff?��S �Ms?�'wnq�l?f0a��/o? Ze���e?x�4A>�x? *r0H��=�f�'\uY?=N&��f?Ow6��&_?�(�l�]?,2T�P? 5��U|?�2��	؍=+�:a���>^L�G�>�k8䟍>'��*E�>�F���f�>Z~���>n]x-�>�AJQ��>Bɥ�%@�Q�4�2��Q��C<,@����+@|%����?   DRIFT7      CSRDRIFTs�e� �^?���^J�>��@Cݔ>�8"]f���me�+�bp���rrm�>ӑ¿�a��=N&��f?��@���>
P�M~����y���w���	��>���եA���\�]��[?ƿc��ɾs�p�HP>�=p�`���!&��I�<�(�l�]?���&�e�p�2[P�>��n������=5١P?8؇�ܾ.����< 5��U|?X�͎z���{�؍=�
��}�j?��S �Ms?n��p�Cm?f0a��/o? H�i�e?ض�ة��? ���L��=�l���h�s���.�q�n��p�Cm����p�Uj� (J��S�ض�ة��� �#Z���
��}�j?��S �Ms?oͩ�aWi?f0a��/o? H�i�e?x�4A>�x? ���L��=s�e� �^?=N&��f?�\�]��[?�(�l�]?��=5١P? 5��U|?�{�؍=h�:a���>&L�G�>�n8䟍>���*E�>YF���f�>~���>�m]x-�>JAJQ��>��Ql�0@h��S��6��o~ܒ&@��,,�'@�9jޕ�?   CLA-S02-MAG-HVCOR-03      KICKER�,�N�`?�Ƚa 5�>�H=�d�>, Dv�D���bIq�z��#.9�><r$'P���=N&��f?ε�
�>
P�M~���LK���w���	��>��#�jB����h`�Z?$��f��Ⱦ
Q��M>����7����S�~G��<�(�l�]?�P��\�e�p�2[P�>h�~��*!�/ˡP?X�Ք[�ܾq����< 5��U|?u�帛��H��N!ٍ=z���%�k?��S �Ms?V��d(Tl?f0a��/o? � �e?ض�ة��? R�N��=�_�k��i�s���.�q�V��d(Tl����p�Uj� t�S�ض�ة���  ���z���%�k?��S �Ms?}�1�"�h?f0a��/o? � �e?x�4A>�x? R�N��=�,�N�`?=N&��f?��h`�Z?�(�l�]?*!�/ˡP? 5��U|?H��N!ٍ=T�:a���>�L�G�>�m8䟍>W��*E�>�F���f�>�~���>Bn]x-�>�AJQ��>��,O�u1@p� 6?�7�J�/Ҭ�$@�����'@�b:F�:�?   DRIFT8      CSRDRIFT�C�.w�c?k��A�>8ܕ9h��>B���������4u�s�r׋��>����ܲ�=N&��f?���6�~�>
P�M~�����Ʉ�w���	��>��ȧF��^G;��U?�ґO3/ľFt�2�W>>/0D��E�� ��X{<�(�l�]?K�e<w�e�p�2[P�>5'>��c�����(~�P?�딼g�ܾkؕ@��< 5��U|?I�mR��A�(>Rڍ=�+ZӦ	q?��S �Ms?��ɤ,g?f0a��/o? .j��e?ض�ة��? �^T��=�,�|�o�s���.�q���ɤ,g����p�Uj� �EV.S�ض�ة��� ج�'���+ZӦ	q?��S �Ms?���p�2d?f0a��/o? .j��e?x�4A>�x? �^T��=�C�.w�c?=N&��f?^G;��U?�(�l�]?���(~�P? 5��U|?A�(>Rڍ=+�:a���>^L�G�>�k8䟍>'��*E�>wF���f�>:~���>�m]x-�>lAJQ��>� ��AI:@D���m=����`@7\5D��"@�b:F�:�?   CLA-S02-DIA-SCR-02-W      WATCH�C�.w�c?k��A�>8ܕ9h��>B���������4u�s�r׋��>����ܲ�=N&��f?���6�~�>
P�M~�����Ʉ�w���	��>��ȧF��^G;��U?�ґO3/ľFt�2�W>>/0D��E�� ��X{<�(�l�]?K�e<w�e�p�2[P�>5'>��c�����(~�P?�딼g�ܾkؕ@��< 5��U|?I�mR��A�(>Rڍ=�+ZӦ	q?��S �Ms?��ɤ,g?f0a��/o? .j��e?ض�ة��? �^T��=�,�|�o�s���.�q���ɤ,g����p�Uj� �EV.S�ض�ة��� ج�'���+ZӦ	q?��S �Ms?���p�2d?f0a��/o? .j��e?x�4A>�x? �^T��=�C�.w�c?=N&��f?^G;��U?�(�l�]?���(~�P? 5��U|?A�(>Rڍ=+�:a���>^L�G�>�k8䟍>'��*E�>wF���f�>:~���>�m]x-�>lAJQ��>� ��AI:@D���m=����`@7\5D��"@��[�E��?   DRIFT9      CSRDRIFTW�UPg?K�_C���>D
ؐ��>�)�K�����M�y�x�-�7O���>�qR� ��=N&��f?6�x�6�>
P�M~��q>#�w���	��>CNZA�J��B�|��%Q?�:��$ο� d����>��Q�yr�FrcP�I<�(�l�]?d�0��ve�p�2[P�>Vq���J���1�Q7�P?�&p��ܾ�;�oC�< 5��U|?���;�����>�lۍ= 9Y%��s?��S �Ms?���}ib?f0a��/o? �%��e?ض�ة��? ��:Z��=����g�r�s���.�q����}ib����p�Uj� ���S�ض�ة��� Ĩ��"�� 9Y%��s?��S �Ms?XY���-`?f0a��/o? �%��e?x�4A>�x? ��:Z��=W�UPg?=N&��f?B�|��%Q?�(�l�]?�1�Q7�P? 5��U|?��>�lۍ=T�:a���>�L�G�>�m8䟍>V��*E�>�F���f�>J~���>�m]x-�>{AJQ��>�fsXB@�v�;A�nl)�*@-����@�Ц�t��?   CLA-S02-MAG-QUAD-03      KQUAD�� �f?_�h0��ZYL�vޘ>�a��>��>P2��x�T��"�>�޻����g���Ko?ʏǘ����R��`&��2�cR���>7{�5K����t�S��<�l���{O?Eμ��˛>���`��2�+,Ә�]�cX%�>�p�fri��@?�=?�־f�\�f�_�>�˾G�k���s��7�P?lM�Y�ܾ}qo��	�<G��U|?M0k&���1�y�܍=Q@c�ls?Z�.�y{?Z>� m�`?���,�P? X�ə�e?���ة��? �
z���=b����r�Z�.�y{�Z>� m�`�<�/�WP� <H)�S����ة��� �U^�$��Q@c�ls?E�;�y?UFFl ^?���,�P? X�ə�e?ԣ?A>�x? �
z���=�� �f?g���Ko?�l���{O?fri��@?�s��7�P?G��U|?�1�y�܍=�����>U4B�>O��}��>��V���>�HU~l�>�ܸ�X��>�u�/��>��:�U�>�q��89@��G�Z�A@&�Hc�@M�y)]����58�'�@   DRIFT10      CSRDRIFTYt|c��[?�Hz�R۾�&��m�>}y���Δ>g��)n�
�j���>�%�Y��g���Ko?5As}��R��`&���T��¨�>7{�5K���2��<��!���Q?�� 6:�>3b��s|Q�]/� �Ti>(7Y��Z��fri��@?}9�:P�f�\�f�_�>��d�����)9�U�P?+�o�M�ܾ�Y�!�<G��U|?f%1������0)�ߍ=�R�|^h?Z�.�y{?���z�5c?���,�P? ��)�e?���ة��? ��aD��=z0^��f�Z�.�y{����z�5c�<�/�WP� �.`#S����ة��� l���-���R�|^h?E�;�y?$��2Ya?���,�P? ��)�e?ԣ?A>�x? ��aD��=Yt|c��[?g���Ko?��!���Q?fri��@?�)9�U�P?G��U|?��0)�ߍ=l����>W 4B�>��}��>��V���>�HU~l�>�ܸ�X��>�u�/��>��:�U�>4���v#@���5@�̘��@�-�Yx��~����@   CLA-S02-MAG-QUAD-04      KQUAD�
#��=V?�@K��þ�;�ntؑ>�N.㘒~�+u��h���o�B�>޺ˠA�����1�f�\?�؂0�
���L * �|>�ҀW�*n>��'�����xGu�<�e�:gQ?�	}��ͱ�l�k�:�U��Br> �t>��.����'"Q?��#�#,S���~��Љ>��A�sB��b*on�P?�*�!�ܾ�F����<����U|?d�|�����ˏS�=ąwy��c?�aQ3�j?���x�b?=k���a? `��K�e?��ة��? pKI���=t��6#b��aQ3�j����x�b���ݛ^� �2Г%S���ة��� X�0��ąwy��c?�C�3�h?Ċ�1��`?=k���a? `��K�e?>?A>�x? pKI���=�
#��=V?��1�f�\?�e�:gQ?'"Q?b*on�P?����U|?��ˏS�=�Q��8�>09�@�>� �r/4�>��,h�>'l3T.�>s���:��>������>�b��p��>�C^��@�ϐ6� @Y�+�=@��E��@�=xD�@   DRIFT11      CSRDRIFT�[�R�;U?���#�¾� ؐ>|�(ҍ}�-��jg�q\~%@�>�tGd�����1�f�\?xixZɔ��L * �|>�1j��+n>��'�����hf��<I�GWY�P?h�}�/(��Wxٌ�xV��ڪ�v>a>f,)��'"Q?�7��G)S���~��Љ>u1�g>@����u q�P?"L���ܾa���8�<����U|?.��
��$��Ƕ�=�Hq��b?�aQ3�j?�x�P�a?=k���a? ��9-�e?��ة��? �f�Ʉ�=�k��H\a��aQ3�j��x�P�a���ݛ^�  �6�%S���ة��� ����0���Hq��b?�C�3�h?*o9֞\`?=k���a? ��9-�e?>?A>�x? �f�Ʉ�=�[�R�;U?��1�f�\?I�GWY�P?'"Q?��u q�P?����U|?$��Ƕ�=�Q��8�>09�@�>� �r/4�>��,h�>.l3T.�>{���:��>������>�b��p��>�?��fw@��nt'�@�	�f#@6���/@�=xD�@   CLA-C2V-MARK-01      WATCH�[�R�;U?���#�¾� ؐ>|�(ҍ}�-��jg�q\~%@�>�tGd�����1�f�\?xixZɔ��L * �|>�1j��+n>��'�����hf��<I�GWY�P?h�}�/(��Wxٌ�xV��ڪ�v>a>f,)��'"Q?�7��G)S���~��Љ>u1�g>@����u q�P?"L���ܾa���8�<����U|?.��
��$��Ƕ�=�Hq��b?�aQ3�j?�x�P�a?=k���a? ��9-�e?��ة��? �f�Ʉ�=�k��H\a��aQ3�j��x�P�a���ݛ^�  �6�%S���ة��� ����0���Hq��b?�C�3�h?*o9֞\`?=k���a? ��9-�e?>?A>�x? �f�Ʉ�=�[�R�;U?��1�f�\?I�GWY�P?'"Q?��u q�P?����U|?$��Ƕ�=�Q��8�>09�@�>� �r/4�>��,h�>.l3T.�>{���:��>������>�b��p��>�?��fw@��nt'�@�	�f#@6���/@�=xD�@   END      WATCH�[�R�;U?���#�¾� ؐ>|�(ҍ}�-��jg�q\~%@�>�tGd�����1�f�\?xixZɔ��L * �|>�1j��+n>��'�����hf��<I�GWY�P?h�}�/(��Wxٌ�xV��ڪ�v>a>f,)��'"Q?�7��G)S���~��Љ>u1�g>@����u q�P?"L���ܾa���8�<����U|?.��
��$��Ƕ�=�Hq��b?�aQ3�j?�x�P�a?=k���a? ��9-�e?��ة��? �f�Ʉ�=�k��H\a��aQ3�j��x�P�a���ݛ^�  �6�%S���ة��� ����0���Hq��b?�C�3�h?*o9֞\`?=k���a? ��9-�e?>?A>�x? �f�Ʉ�=�[�R�;U?��1�f�\?I�GWY�P?'"Q?��u q�P?����U|?$��Ƕ�=�Q��8�>09�@�>� �r/4�>��,h�>.l3T.�>{���:��>������>�b��p��>�?��fw@��nt'�@�	�f#@6���/@