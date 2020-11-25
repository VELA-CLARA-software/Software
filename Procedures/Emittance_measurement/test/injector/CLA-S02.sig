SDDS1
!# little-endian
&description text="sigma matrix--input: CLA-S02.ele  lattice: CLA-S02.lte", contents="sigma matrix", &end
&parameter name=Step, description="Simulation step", type=long, &end
&parameter name=SVNVersion, description="SVN version number", type=string, fixed_value=26940M, &end
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
                 _BEG_      MARK%�K��?��o�:N?I_-�Q�C?���ã�'?�}��(^w?A��X�E6
�=[���?}k�YaL3?p��@�x)?�=�鏻}?8�W�ߣc��7W�Vź=]x��
�?�>}Qf5S?��u�Q�^�7���3[?if�j�ϛ�� ����?�d4�}Zh�'��M?�-<�꥽l\�G�?E��t5���U�A��>F������?�|�i�d�I(Y��/>���^V�?�!���?�{Lh�d�?�q�$H.�?� �C�@��N���?�ev4;@>���^V¿ʆWn�L����捯���q�$H.¿�[柱ϸ���N����FAU�T����-Z���?�!���?�{Lh�d�?�7���?� �C�@�����?�ev4;@>%�K��?[���?]x��
�?� ����?l\�G�?F������?I(Y��/>�҆*�M?��81��?F��'�_C?>!\Xo��?t-��R?�ƣ�C�?)�`/�Q?l��Xa�?}<��;�@�S
ͺH��1�%��@:i&�S�           START      CHARGE%�K��?��o�:N?I_-�Q�C?���ã�'?�}��(^w?A��X�E6
�=[���?}k�YaL3?p��@�x)?�=�鏻}?8�W�ߣc��7W�Vź=]x��
�?�>}Qf5S?��u�Q�^�7���3[?if�j�ϛ�� ����?�d4�}Zh�'��M?�-<�꥽l\�G�?E��t5���U�A��>F������?�|�i�d�I(Y��/>���^V�?�!���?�{Lh�d�?�q�$H.�?� �C�@��N���?�ev4;@>���^V¿ʆWn�L����捯���q�$H.¿�[柱ϸ���N����FAU�T����-Z���?�!���?�{Lh�d�?�7���?� �C�@�����?�ev4;@>%�K��?[���?]x��
�?� ����?l\�G�?F������?I(Y��/>�҆*�M?��81��?F��'�_C?>!\Xo��?t-��R?�ƣ�C�?)�`/�Q?l��Xa�?}<��;�@�S
ͺH��1�%��@:i&�S�           CLA-S02-APER-01      MAXAMP� x��rq?�e^��>˦�tVd��P,���ھYо;V�>h*(nD羾��)����<c��M?�(��q@ؾe釘�F�����|�u>;��	ZE������m�<,�H���|?�Z�����>�? �>�¢��Ӿ�g�O2�<�5��j~Z?t����v> ���D������<֦�^�N8?����BH��m�-͉�<����]"h?E�#�_��a�u�u=�f�v�?!��Y�0a?���*��?̈6��i?�?
3�=?�����n?��V�p�z=��=�]پc�R<�����*�ꋿ̈6��i�A^����=������n��ɓ��|z��f�v�?!��Y�0a?P�g��d?՞���@?�?
3�=?PC$���k?��V�p�z=� x��rq?c��M?,�H���|?�5��j~Z?֦�^�N8?����]"h?�a�u�u=SI���[z>�5*Z�>                !z�����>�],��,�>                                                9	�/���?   CLA-S02-MAG-HVCOR-01      KICKER��%�q?�ľ|��>�D��a��x�f0j۾���җ>�e�R�{��B��dW�<c��M?�⫂��ؾe釘�F���).��u>;��	ZE�����`|�<Cwcؐ{}?����h�>�oA�U�>ѯE>$Ծv9ɋ~�<�5��j~Z?%�PW5�v> ���D���w3�}�<�l>O8?Ž��H���a =��<����]"h?�lQ&�`���A�u=�����ʄ?!��Y�0a?(t^�h�?̈6��i? �0�=�=?�����n? M�z=0T��پc�R<��(t^�h��̈6��i� 5��+�=������n� +<��z������ʄ?!��Y�0a?>dB]�nd?՞���@? �0�=�=?PC$���k? M�z=��%�q?c��M?Cwcؐ{}?�5��j~Z?�l>O8?����]"h?���A�u=vU���[z>>*Z�>�k���{7=~!2�Y�=������>��,��,�>                ��?�.�A�Cg��                9�bԵ��?   DRIFT1      CSRDRIFT������q?�!la$6�>��>����KL+"�۾�n&���>�P�@R�����,؁�<c��M?��G��ؾe釘�F���-��*�u>;��	ZE���K�ҁ�<�þ�B�}?3\wՐ�>q��gt�>_AHN�CԾ�s���<�5��j~Z?Sgv���v> ���D���q3�]u�<�;x�O8?/��H
H���#�&ǋ�<����]"h?��/
]a�V/r���u=-�*�x�?!��Y�0a?���*��?̈6��i? ��/�=?�����n? ߞ��z=��l�h ھc�R<�����*���̈6��i� ���\�=������n� ��r�z�-�*�x�?!��Y�0a?2�C"�d?՞���@? ��/�=?PC$���k? ߞ��z=������q?c��M?�þ�B�}?�5��j~Z?�;x�O8?����]"h?V/r���u=�K���[z>Y7*Z�>�!� P=��ws=!z�����>�],��,�>                �A~��A��}^ɂ��                $狽_�?   CLA-S02-MAG-QUAD-01      KQUAD^���V2s?@Qz�=w�>7wm�� �/�����>�~�Xk��>��[ ����3.��<l!Z ӹw?�%�!������'��?�2���Ϡ>�5T��ž��98!�<���F��|?����0��Wm�S�>g����Ӿ);��m��<��Lm�y?P�]�,��M$p��>}R<��Լ���Q�P8?�B��F��R��ď�<����]"h? i�!�a𼝘L��u=C�N��?~���ދ?ȫ\���?��7방�? ���+�=?�����n? ��ȿz=��O�ܾ����6��ȫ\������c|,b� ��<�=������n� `�}�z�C�N��?~���ދ?�pk���c?��7방�? ���+�=?PC$���k? ��ȿz=^���V2s?l!Z ӹw?���F��|?��Lm�y?���Q�P8?����]"h?��L��u=ꀻgs*�>�z逓��>��f9X=�>ƽ�ݰ=�|�Ѝ�>nS4Q͞�>����na=vǧ�rF�=7�0��A%J���`���C�l�A��U
�A2`��i�?   CLA-S02-DIA-BPM-01      MONI���[Et?�J5�>rA��9 ���h/�>�Cm�mX�>=pH ¾K��tL�<l!Z ӹw?³�e������'��?1�Ͼw�>�5T��ž�:���N�<��=�{?�nڲ��qAf���>�;��Ҿ%D��i�<��Lm�y?�I�j#���M$p��>����K�ӼM+XUS8?>���D��C����<����]"h?�.O��`�ŀ����u=�ºD_ȇ?~���ދ?k��}.��?��7방�? Xٕ�=?�����n? �����z=p]���ݾ����6��k��}.�����c|,b� Xٕ�=������n� �����z��ºD_ȇ?~���ދ?c���Nc?��7방�? `[Zr�=?PC$���k? �WJ�z=���[Et?l!Z ӹw?��=�{?��Lm�y?M+XUS8?����]"h?ŀ����u=:�gs*�>��耓��>                ��{�Ѝ�>�=3Q͞�>                                                1%Y��+�?   DRIFT2      CSRDRIFT6�ܷ8Lz?�d�9x?1�Τ� �#䩕��?ܞ�+1�>U4ѤQ�Ǿ������<l!Z ӹw?����z������'��?~w��%�>�5T��ž1�ƚ���<O]RT�u?�c�� �O�%v_�>l�E���̾�l�|?�<��Lm�y?�\Gv;���M$p��>#�~b�ȼ�J[�k8?��oz:��{t��e��<����]"h?Hz�[�I�QG�u=�̶P�܎?~���ދ?p�`I�?��7방�? �t��>?�����n? Ԑy̮{=����P�����6��p�`I����c|,b� �t��>������n� Ԑy̮{��̶P�܎?~���ދ?����\?��7방�? 83���<?PC$���k? �?�y=6�ܷ8Lz?l!Z ӹw?O]RT�u?��Lm�y?�J[�k8?����]"h?I�QG�u=���gs*�>W+ꀓ��>=��ګ'd=��b���=��{�Ѝ�>�=3Q͞�>                i$+�sƐAM2VA��                ��/��d�?   CLA-S02-MAG-QUAD-02      KQUADk��җ{??���7�>�fm����.!K�>8ȗ>�>�����Ⱦ�6a${�<�'���A=?��G��2��q[-��>E넗��l>#!�۲9���T�"p��<H���Ds?�=����澏z��n�> ��q�ʾXЭVu�<ЂS�a�b?�]��+9t��7s��(�>�-�Դ;���1�:q8?�Y��8���ۑ,���<����]"h?�ö�\�D�	��u=�̽�?1�?e��SMQ?��ň��?R���#r?  ,�.??�����n? `9f7�{=�t��J侥Rn������ň���K���]SL�  ,�.?������n� `9f7�{��̽�?1�?e��SMQ?�CbMJZ?R���#r? ?Q�<?PC$���k? �%��y=k��җ{?�'���A=?H���Ds?ЂS�a�b?�1�:q8?����]"h?D�	��u=~�Bu��v>�[��s�>�U��=0�B�s=�$G�G�>�p�?���>^3��L@=���`��=a�����A��2�^��W�ܐϡ�A/rDC�?�AI�����?   DRIFT3      CSRDRIFT��@�b�{?䰏�g�>�O�n�k����d,��>O"���d�>;�#ڣɾ�R��{��<�'���A=?!�b����q[-��>�uܗ�m>#!�۲9��/z��<�=�?�3r?ef[֘�e�'���>6oQ�Ⱦݓ��/�<ЂS�a�b?���`�s��7s��(�>i��y�������%r8?��zW8����Lc���<����]"h?q8���]��Y���u=n1הXP�?e��SMQ?O�3����?R���#r? h���	??�����n? �z-�{=�$��y侥Rn����O�3�����K���]SL� h���	?������n� �z-�{�n1הXP�?e��SMQ?I�*�X?R���#r? �n�S�<?PC$���k?  .}��y=��@�b�{?�'���A=?�=�?�3r?ЂS�a�b?����%r8?����]"h?�Y���u=T�Bu��v>�[��s�>�8��ۊ*='�2�z�=�G�G�>�g�?���>N��w#=fg��{=�|}�v�AZ�u��э�.b�R*+�AG�a8 ϰAI�����?   CLA-S02-DIA-SCR-01      WATCH��@�b�{?䰏�g�>�O�n�k����d,��>O"���d�>;�#ڣɾ�R��{��<�'���A=?!�b����q[-��>�uܗ�m>#!�۲9��/z��<�=�?�3r?ef[֘�e�'���>6oQ�Ⱦݓ��/�<ЂS�a�b?���`�s��7s��(�>i��y�������%r8?��zW8����Lc���<����]"h?q8���]��Y���u=n1הXP�?e��SMQ?O�3����?R���#r? h���	??�����n? �z-�{=�$��y侥Rn����O�3�����K���]SL� h���	?������n� �z-�{�n1הXP�?e��SMQ?I�*�X?R���#r? �n�S�<?PC$���k?  .}��y=��@�b�{?�'���A=?�=�?�3r?ЂS�a�b?����%r8?����]"h?�Y���u=T�Bu��v>�[��s�>�8��ۊ*='�2�z�=�G�G�>�g�?���>N��w#=fg��{=�|}�v�AZ�u��э�.b�R*+�AG�a8 ϰA����)��?   DRIFT4      CSRDRIFTr)�|?of�3��>ÉȤ�k����Uus��> �H�ҩ>�X��\ɾ�I�̾*�<�'���A=?pG���B��q[-��>	�2@m>#!�۲9���`$��>�<F�$���p?4�_[��U�%�=|>؉i3��ƾPD;q���<ЂS�a�b?�C��us��7s��(�>!p)#�����as8?����7���3��<����]"h?��Ւ�_�R|��/�u=��=by�?e��SMQ?Mk�ǜ<�?R���#r? Hzp�??�����n? ��� �{=3� ��侥Rn����Mk�ǜ<��K���]SL� Hzp�?������n� ��� �{���=by�?e��SMQ?������V?R���#r? B�l�<?PC$���k? �d4�y=r)�|?�'���A=?F�$���p?ЂS�a�b?��as8?����]"h?R|��/�u=T�Bu��v>�[��s�>�8��ۊ*='�2�z�=�G�G�>�g�?���>��{���(=M�[�U�=K��E��AA>�Ķ��y2��ѵANyT���Ay"1��?   CLA-S02-MAG-HVCOR-02      KICKER5����|?��H�
��>����럔}���>�J��>�-	��kɾ�M ?�<�'���A=?km�ɻ�q[-��>pab,�Hm>#!�۲9���XD�G�<��㫂p?�-1�ؖ��f/<�{>�5�[� ƾ��4'��<ЂS�a�b?��Ct_s��7s��(�>/uьz����r�s8?5F�p�7��x������<����]"h?t�`�&f\�u=w(�P���?e��SMQ?�^����?R���#r?  :�??�����n? �D�e�{=e�и\�侥Rn�����^�����K���]SL�  :�?������n� �D�e�{�w(�P���?e��SMQ?�@C�,V?R���#r? h�aӪ<?PC$���k?  �8��y=5����|?�'���A=?��㫂p?ЂS�a�b?�r�s8?����]"h?&f\�u=T�Bu��v>�[��s�>�8��ۊ*='�2�z�=�G�G�>>U�?���>                �E�!�A���l�*��                ��|��?   DRIFT5      CSRDRIFT`�q�#C|?H��_��>S��$����k&X�>�,5f�!�>�*xbo�ɾ�R;4�r�<�'���A=?u9����q[-��>�hi^m>#!�۲9���i�D}[�<�Qg�/�o?W��\���Dު��y><�8�	ž���!K�<ЂS�a�b?�����&s��7s��(�>Z�Q�X�����OFt8?�|$�7��&͗f��<����]"h?e���/a�m�AN�u=�w�|���?e��SMQ?�1�4&�~?R���#r? ೬>??�����n? ��l�{=�[l�k�侥Rn�����1�4&�~�K���]SL� ೬>?������n� ��l�{��w�|���?e��SMQ?Ǝ��U?R���#r? x2I̦<?PC$���k? ���y=`�q�#C|?�'���A=?�Qg�/�o?ЂS�a�b?���OFt8?����]"h?m�AN�u=��Bu��v>/�[��s�>                �G�G�>>U�?���>                                                v؜�'�?   CLA-S02-COL-01      ECOL���3y�`?�:�k�j�>`��a�ذ>z�2D3����3�e��>iҋ��޾��*`���<�����"?" ���r>�X�G�p��	��rq>h��O�2���]:`�j�<&=�5@?҄^b�̌��^���E�>?9�ݞ׽�
���A�<R
��m<?$;�󊊾Jތ�5*�>Ю�h��Ǽ �<�=?�~�𾀻�R�P��<�d�Utm?Ng�o��� �?���z=ǻ܌��p?�����2?���i�%P?K���]SL? �<�=?�d�Utm? �?���z=7n�Mq徥Rn����8G3T�оK���]SL� �<�=��d�Utm� �?���z�ǻ܌��p?�����2?���i�%P?�D���>  �<�=?�d�Utm? �?���z=���3y�`?�����"?&=�5@?R
��m<? �<�=?�d�Utm? �?���z=                �%e�a�<��4rF3H=                ���=��<��n��A=        �d�UtM������T>       �v؜�'�?   CLA-S02-APER-02      MAXAMP���3y�`?�:�k�j�>`��a�ذ>z�2D3����3�e��>iҋ��޾��*`���<�����"?" ���r>�X�G�p��	��rq>h��O�2���]:`�j�<&=�5@?҄^b�̌��^���E�>?9�ݞ׽�
���A�<R
��m<?$;�󊊾Jތ�5*�>Ю�h��Ǽ �<�=?�~�𾀻�R�P��<�d�Utm?Ng�o��� �?���z=ǻ܌��p?�����2?���i�%P?K���]SL? �<�=?�d�Utm? �?���z=7n�Mq徥Rn����8G3T�оK���]SL� �<�=��d�Utm� �?���z�ǻ܌��p?�����2?���i�%P?�D���>  �<�=?�d�Utm? �?���z=���3y�`?�����"?&=�5@?R
��m<? �<�=?�d�Utm? �?���z=                �%e�a�<��4rF3H=                ���=��<��n��A=        �d�UtM������T>       ��BY���?   DRIFT6      CSRDRIFTV����`?��+���>��C��X�>DL�ʭ�kw$�qQ�>E.
]��޾��_9�5�<�����"?��mEX�p>�X�G�p�r6�rq>h��O�2���vb�&o�<*����<?���\��������	�>3�Cצ���J^�Z�<R
��m<?�U�S���Jތ�5*�>[o=)�Ǽ P:��=?S%�"�����Bc"�<�d�Utm?s	��m��� x�V��z=+�^P�p?�����2?�8/���L?K���]SL? P:��=?�d�Utm? ��V��z=�T��n�徥Rn����쟱�l�̾K���]SL� P:��=��d�Utm� p�V��z�+�^P�p?�����2?�8/���L?�D���> P:��=?�d�Utm? ��V��z=V����`?�����"?*����<?R
��m<? P:��=?�d�Utm? x�V��z=                                                                                                W@ܕ�?   CLA-S02-MAG-HVCOR-03      KICKER`���`?B��@���>�1�Ӄ�>�^��ڭ����)Nb�>�)�;_�޾P�*i�E�<�����"?LL���hp>�X�G�p�x���rq>h��O�2���#<�6p�<���/<?�d������6bi�=�>\Ug�ݹ��{��<R
��m<?L`�k���Jތ�5*�>r�P��Ǽ P����=?ɧ�J;���䞹!S#�<�d�Utm?&�|�C��� ��/z�z=^a<�p?�����2?E����K?K���]SL? P����=?�d�Utm? ��/z�z=��.į徥Rn��������4̾K���]SL� P����=��d�Utm� ��/z�z�^a<�p?�����2?E����K?�D���> P����=?�d�Utm? ��/z�z=`���`?�����"?���/<?R
��m<? P����=?�d�Utm? ��/z�z=      �<��yrFF=                                                                                ��g�:�?   DRIFT7      CSRDRIFTF��BO�`?2���ٓ>=��ܨ>�b���2��~C�2��>��JUJ߾�Cv/[��<�����"?d[f-Uk>�X�G�p�iZ�9sq>h��O�2��xDp�v�<���>�g7?���[ʄ���{�Vۅ>)nR�ኵ���V����<R
��m<?P.*�Jތ�5*�>w
L�E�Ǽ P�V�=?m)������|(�<�d�Utm?�$������ x&�|�z=�n!hU�p?�����2?X��OG?K���]SL? P�V�=?�d�Utm? �&�|�z=�@�P��徥Rn����c
	+�ǾK���]SL� P�V�=��d�Utm� �&�|�z��n!hU�p?�����2?X��OG?�D���> P�V�=?�d�Utm? p&�|�z=F��BO�`?�����"?���>�g7?R
��m<? P�V�=?�d�Utm? x&�|�z=                                      �<��yrF6=                                                ��g�:�?   CLA-S02-DIA-SCR-02      WATCHF��BO�`?2���ٓ>=��ܨ>�b���2��~C�2��>��JUJ߾�Cv/[��<�����"?d[f-Uk>�X�G�p�iZ�9sq>h��O�2��xDp�v�<���>�g7?���[ʄ���{�Vۅ>)nR�ኵ���V����<R
��m<?P.*�Jތ�5*�>w
L�E�Ǽ P�V�=?m)������|(�<�d�Utm?�$������ x&�|�z=�n!hU�p?�����2?X��OG?K���]SL? P�V�=?�d�Utm? �&�|�z=�@�P��徥Rn����c
	+�ǾK���]SL� P�V�=��d�Utm� �&�|�z��n!hU�p?�����2?X��OG?�D���> P�V�=?�d�Utm? p&�|�z=F��BO�`?�����"?���>�g7?R
��m<? P�V�=?�d�Utm? x&�|�z=                                      �<��yrF6=                                                a_y����?   DRIFT8      CSRDRIFT�̿��0a?G
n��>��<��>��7�؊��ƺ~?�>�]Y���߾�aO��<�����"?
�w��e>�X�G�p��2ďsq>h��O�2���� �{�<ܾ����2?��ťv����ɦ$�s�>c��-3����5J|�<R
��m<?��Aq���Jތ�5*�>���ֽ�Ǽ P�M��=?��sbJ���+޹�-�<�d�Utm?iZ�_���� (5'��z=
��%q?�����2?�t?�	�B?K���]SL? P�M��=?�d�Utm? 05'��z=O��7澥Rn�����J��þK���]SL� P�M��=��d�Utm�  5'��z�
��%q?�����2?�t?�	�B?�D���> P�M��=?�d�Utm? 05'��z=�̿��0a?�����"?ܾ����2?R
��m<? P�M��=?�d�Utm? (5'��z=                                      �<��yrF6=                                                ��*�?   CLA-S02-MAG-QUAD-03      KQUAD��	@k`?�'JSHؾ��V�4�>�vv�:j�jl��2�>G�{Y�zݾ4|h�<^_8$Ch? M`�����-�ٷ�s>�e~������&�U�>�Gg�v�����11?��'ڠ(<�N�.���>#�q楯���^�)��<�c��4�>����}H��r�*Hx>������� �ݫ��=?,� ˆ����O�r8�<�d�Utm?�J�j��� X�7��z=��G��o?�7L�3x?��g�A?�Mc�^
? �ݫ��=?�d�Utm? `�7��z=��˴�価7L�3x��	���¾�Mc�^
� �ݫ��=��d�Utm� `�7��z���G��o?I{O��	�>��g�A?r`��є� �ݫ��=?�d�Utm? P�7��z=��	@k`?^_8$Ch?���11?�c��4�> �ݫ��=?�d�Utm? X�7��z=�;f��6=�y�y��=                                                                                ��o{��@   DRIFT9      CSRDRIFT�y4UـQ?:���ʾª	EE�>r��BU�\���_Z�s�>P�W�fо�-�%���<^_8$Ch?��hS���-�ٷ�s>h^�.�Ͷ���&�U�>T�k
���+�����0?6�i[;�-#=�'e>aN޾�� 1�\�<�c��4�>=�;��H��r�*Hx>t0{��@�� ���>?W�!�"���^�_����<�d�Utm?����� h�
,{=�:��kua?�7L�3x?���=�@?�Mc�^
? ���>?�d�Utm? p�
,{=v}���־�7L�3x����Oþ�Mc�^
� ���>��d�Utm� `�
,{��:��kua?I{O��	�>���=�@?r`��є� ���>?�d�Utm? p�
,{=�y4UـQ?^_8$Ch?+�����0?�c��4�> ���>?�d�Utm? h�
,{=                ���=�(=��n���=                                �����4������T>                =��H�r@   CLA-S02-MAG-QUAD-04      KQUAD.K�ˋM?��jOx���u�!ˋ�>Ó�����Ex�ʛ>>��2˾�8���<�9aٕ;?��W.��x�Q�"NÒ>j���a��*�d�>��U�6sǼ���a6�,?����>���N%n�{>�o[��v���P ��p�<�ҍ��E?�[�0	y��M�%��>���~��Ҽ yMg>?�M�q�����K��<�d�Utm?��[��	�� ����3{=W{B�cx]?gO��K?�_~��<?T��|��U?  yMg>?�d�Utm? ����3{=�֛�gӾgO��K�Um�"���T��|��U�  yMg>��d�Utm� ����3{�W{B�cx]?Ws;L#ҿ>�_~��<?.��m�>  yMg>?�d�Utm? ����3{=.K�ˋM?�9aٕ;?���a6�,?�ҍ��E? yMg>?�d�Utm? ����3{=                                                ���=��<��n��A=                �����$�       �S��D�%@   DRIFT10      CSRDRIFTQ�@'0�C?,F*6������������)��QӚ�w"�[ڐ�>�1Û&¾��j��<�9aٕ;?�Q^��|>Q�"NÒ>�&YY�����*�d�>ɼ�Ǽ�r�0?�uZ��>N{�T�گ`9��>����d���ҍ��E?(]<�~��M�%��>2=^�Ҽ �� >?pڻ�2���n��N���<�d�Utm?&�%)�!�� ����M{=U�	zs�S?gO��K?�n� ��@?T��|��U?  �� >?�d�Utm? ����M{=��}mZy˾gO��K��n� ��@�T��|��U�  �� >��d�Utm� ����M{�U�	zs�S?Ws;L#ҿ>��9漆�>.��m�>  �� >?�d�Utm? ����M{=Q�@'0�C?�9aٕ;?�r�0?�ҍ��E? �� >?�d�Utm? ����M{=                                                                                                �{+�@   CLA-S02-MAG-QUAD-05      KQUAD%4��]E?�M�r��>�;��Qs��T��
�}>ۨ��~�>iE����þd�}H�=�<�羓~�W?��g��gyI��>q+$�H�>�����վ��>":4�<��XCO2?2F��i��2F�=��|l9�dڰ>���+C������c&?x�I%u> E�߽������;�< �:�!>?��*�7���Mr�um��<�d�Utm?�UK%�� ���Q{=9x)̵NU?���W6�g?l�o=B?���pW6? �:�!>?�d�Utm? ���Q{=��w�cξ��;�;H�l�o=B��󄁨� �:�!>��d�Utm� ���Q{�9x)̵NU?���W6�g?�Sy����>���pW6? �:�!>?�d�Utm? ���Q{=%4��]E?�羓~�W?��XCO2?����c&? �:�!>?�d�Utm? ���Q{=�;f��=�y�y�_=�;f��=�y�y�_=�;f���<�y�y�=                �;f��F>       �                ��B=]	@   CLA-S02-DIA-BPM-02      MONI�����G?�=�b��>G�Zx`��uy@\��>NGM��i�>zŧY�ž�J#RS�<�羓~�W?�=S�_;��gyI��>�ͩA6J�>�����վ�8��u6�<g����1?�S$,$�h�v�թ�����e�R�>J�'L@K������c&?f�Y�iu> E�߽���SY�zX�< 0�+�#>?v��⽻���,�ѽ�<�d�Utm?Κ�(�� p6#�T{= ��$�W?���W6�g?ko[W��A?���pW6? @�+�#>?�d�Utm? �6#�T{=^��B��о��;�;H�ko[W��A��󄁨� @�+�#>��d�Utm� �6#�T{� ��$�W?���W6�g?��66q��>���pW6?  �+�#>?�d�Utm? `6#�T{=�����G?�羓~�W?g����1?����c&? 0�+�#>?�d�Utm? p6#�T{=                                �;f���<�y�y�=�;f���<�y�y�=                               � D���	@   DRIFT11      CSRDRIFT�j����I?���x��>����͋�ڭ�l��>>Z"��C�>�/�;l�Ǿ�����<�羓~�W?|vMY����gyI��>��4KK�>�����վ�4�OC8�<��a^E1?�r���*h�l`�E��\`��M˯>c��>�������c&?�J.�ou> E�߽���)��!�<  �|%>?"��E;������]��<�d�Utm?)R�6Q*�� �|�W{=�孷�Y?���W6�g?x�4A?���pW6?  �|%>?�d�Utm? �|�W{=����'@Ҿ��;�;H�x�4A��󄁨�  �|%>��d�Utm� �|�W{��孷�Y?���W6�g?=�vB�>���pW6?  �|%>?�d�Utm? �|�W{=�j����I?�羓~�W?��a^E1?����c&?  �|%>?�d�Utm? �|�W{=                �%e�a=��4rF3h=                                �d�Ut=>       �                 D���	@   CLA-S02-DIA-SCR-03      WATCH�j����I?���x��>����͋�ڭ�l��>>Z"��C�>�/�;l�Ǿ�����<�羓~�W?|vMY����gyI��>��4KK�>�����վ�4�OC8�<��a^E1?�r���*h�l`�E��\`��M˯>c��>�������c&?�J.�ou> E�߽���)��!�<  �|%>?"��E;������]��<�d�Utm?)R�6Q*�� �|�W{=�孷�Y?���W6�g?x�4A?���pW6?  �|%>?�d�Utm? �|�W{=����'@Ҿ��;�;H�x�4A��󄁨�  �|%>��d�Utm� �|�W{��孷�Y?���W6�g?=�vB�>���pW6?  �|%>?�d�Utm? �|�W{=�j����I?�羓~�W?��a^E1?����c&?  �|%>?�d�Utm? �|�W{=                �%e�a=��4rF3h=                                �d�Ut=>       �                 D���	@   END      WATCH�j����I?���x��>����͋�ڭ�l��>>Z"��C�>�/�;l�Ǿ�����<�羓~�W?|vMY����gyI��>��4KK�>�����վ�4�OC8�<��a^E1?�r���*h�l`�E��\`��M˯>c��>�������c&?�J.�ou> E�߽���)��!�<  �|%>?"��E;������]��<�d�Utm?)R�6Q*�� �|�W{=�孷�Y?���W6�g?x�4A?���pW6?  �|%>?�d�Utm? �|�W{=����'@Ҿ��;�;H�x�4A��󄁨�  �|%>��d�Utm� �|�W{��孷�Y?���W6�g?=�vB�>���pW6?  �|%>?�d�Utm? �|�W{=�j����I?�羓~�W?��a^E1?����c&?  �|%>?�d�Utm? �|�W{=                �%e�a=��4rF3h=                                �d�Ut=>       �                