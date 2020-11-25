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
                 _BEG_      MARKR�ꡝHi?u����>�AS�n�>�W�TgW>&L�I��>,НG���������<�W�a��J?Kp=56P�>���� K>����f>7�߿%��m��2,�<�]d?�ܥ��O�>��c��>� L�"�Xk�n���<F�̹}E?{�r|��f>�Q��锾5NT�tk�<_c,l�E?�"o:��ǾS(���6�<灕U�q?�#��/r�'5p��a�=�~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��G���?1�<�u�=���5z�$��4B"Y���g�ښp��QHj\2R��G�<�]S���G�����f�""X���~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��q�w?1�<�u�=R�ꡝHi?�W�a��J?�]d?F�̹}E?_c,l�E?灕U�q?'5p��a�=�K�.}>�Kgb�>eVa.�%}>\	'\�>sS��b�x>̼z��o�>T��z�x>P��I�T�>�@�!�U@����7�P����P@k����f1�           START      CHARGER�ꡝHi?u����>�AS�n�>�W�TgW>&L�I��>,НG���������<�W�a��J?Kp=56P�>���� K>����f>7�߿%��m��2,�<�]d?�ܥ��O�>��c��>� L�"�Xk�n���<F�̹}E?{�r|��f>�Q��锾5NT�tk�<_c,l�E?�"o:��ǾS(���6�<灕U�q?�#��/r�'5p��a�=�~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��G���?1�<�u�=���5z�$��4B"Y���g�ښp��QHj\2R��G�<�]S���G�����f�""X���~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��q�w?1�<�u�=R�ꡝHi?�W�a��J?�]d?F�̹}E?_c,l�E?灕U�q?'5p��a�=�K�.}>�Kgb�>eVa.�%}>\	'\�>sS��b�x>̼z��o�>T��z�x>P��I�T�>�@�!�U@����7�P����P@k����f1�           CLA-S02-APER-01      MAXAMPR�ꡝHi?u����>�AS�n�>�W�TgW>&L�I��>,НG���������<�W�a��J?Kp=56P�>���� K>����f>7�߿%��m��2,�<�]d?�ܥ��O�>��c��>� L�"�Xk�n���<F�̹}E?{�r|��f>�Q��锾5NT�tk�<_c,l�E?�"o:��ǾS(���6�<灕U�q?�#��/r�'5p��a�=�~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��G���?1�<�u�=���5z�$��4B"Y���g�ښp��QHj\2R��G�<�]S���G�����f�""X���~Ya'}?�E����]?�����}?�/xx��[?�զ��V?��q�w?1�<�u�=R�ꡝHi?�W�a��J?�]d?F�̹}E?_c,l�E?灕U�q?'5p��a�=�K�.}>�Kgb�>eVa.�%}>\	'\�>sS��b�x>̼z��o�>T��z�x>P��I�T�>�@�!�U@����7�P����P@k����f1�9	�/���?   CLA-S02-MAG-HVCOR-01      KICKER�~��i?M��!�q�># ���,�>���nOqX>�D�Y�^�>JB
�����9��	�<�W�a��J?�ے�uq�>���� K>�;���f>7�߿%���� �,�<N���+�d?Ɲ�o�ݻ>�(;S�n�>"66��X�����*��<F�̹}E?g��5�f>�Q��锾80�nm�<�,�aڣE?TV�8��Ǿd��8W8�<灕U�q?�X�ňs��&���b�=���U�}?�E����]?0|�q�}?�/xx��[?���Y��V?��G���?@}MYw�=�+�l�|z�$��4B"Y�&)�=��p��QHj\2R�@PQ�]S���G����@X�Q�X�����U�}?�E����]?0|�q�}?�/xx��[?���Y��V?��q�w?@}MYw�=�~��i?�W�a��J?N���+�d?F�̹}E?�,�aڣE?灕U�q?�&���b�=�K�.}>�Kgb�>fVa.�%}>\	'\�>sS��b�x>̼z��o�>K��z�x>J��I�T�>����F�V@�%���7�W���0Q@P���1�9�bԵ��?   DRIFT1      CSRDRIFT��d��i?ƢU5B��>���y�t�>Cҝ��X>�*�d]��>�:L���O���>/�<�W�a��J?�_R��}�>���� K>,$+�f>7�߿%�� �/�F-�<ㅜ�d?gʤ��>���阆>|�5`���M�V?�<F�̹}E?g!ϋl�f>�Q��锾l�x�,n�<%.#�գE?��8��ǾJ%gd�8�<灕U�q?�0�
t�^���Zc�=��0�}?�E����]?�~Wx��}?�/xx��[? ����V?��G���?��c��w�=O�6���z�$��4B"Y���+r�q��QHj\2R� ��]S���G�����ܑ^*Y����0�}?�E����]?�~Wx��}?�/xx��[? ����V?��q�w?��c��w�=��d��i?�W�a��J?ㅜ�d?F�̹}E?%.#�գE?灕U�q?^���Zc�=�K�.}>�Kgb�>dVa.�%}>\	'\�>+R��b�x>�z��o�>
��z�x>j��I�T�>�!���W@�;��l�7�  �srQ@�C�:��1�$狽_�?   CLA-S02-MAG-QUAD-01      KQUAD��:#�)l?n���K�>3�,�^�>�o9�+z������c�>�:(��ɥ������<� ����r?��ͣ9�>�?F�+��d�f `Ώ>���?�h�� O�&�<�,��Gd?u���׾��.�f�>i��L�۳�}�x���<���n4b?-�E�Ƴ����|.ɱ>�pi����e���T�E?�"ju<�Ǿ�����9�<灕U�q?�eLLu�I�Y�d�=8Q�a6�?�J�m2�?�c�Wz�|?
����z?�6���V?��G���?�R��w�=j�,�"�|�3�h&�Ȃ�����p�
����z���oB�[S���G���� ��{�X��8Q�a6�?�J�m2�?�c�Wz�|?:iL���m?�6���V?��q�w?�R��w�=��:#�)l?� ����r?�,��Gd?���n4b?e���T�E?灕U�q?I�Y�d�=Ē�a}>�O��K�>�U}�|>����$@�>_���{>Y������>���z�z>u��=W��>��S�N[@ł`���a�����CN@a٨)K@2`��i�?   CLA-S02-DIA-BPM-01      MONI
9m��m?���aC�>�2��R��>N�4��M����C��щ>g�-s��X��$�"�<� ����r?:r�O�>�?F�+���ܨ�3ˏ>���?�h��Ҽ���|�<���Țtc?cB05o!־X"�hs�>"�dF����dZ���<���n4b?"�w�����|.ɱ>ă�����*`ὢE?�z�u�Ǿ0�C�9�<灕U�q?Weznu��z #�d�=�Zˀ,�?�J�m2�?Qj�*�{?
����z? ���V?��G���? *��Sv�=}^�f��~�3�h&�Ȃ�	#��o�
����z� [��YS���G���� ϋUEW���Zˀ,�?�J�m2�?Qj�*�{?:iL���m? ���V?��q�w? *��Sv�=
9m��m?� ����r?���Țtc?���n4b?*`ὢE?灕U�q?�z #�d�=��a}>����K�>��T}�|>0��$@�>�c���{>�������>����z�z>ը�=W��>���CƧ^@D���c�D����K@�v��J@1%Y��+�?   DRIFT2      CSRDRIFT��kT�s? N�u��>��W��ט>A�Ƥ�c�w�@�>qb��tJ��s3�]�Q�<� ����r?��`�>�?F�+��rw�g��>���?�h��p�9�4p�<���H�]?S�N��оH��C��>K���������m�<���n4b?��Xփ���|.ɱ>�X������4�E?�G|��Ǿ����;7�<灕U�q?��?D/v��(��e�=K($d���?�J�m2�?@��l��t?
����z? O��V?��G���? ��>o�=�qMNV��3�h&�Ȃ�E"8h�
����z� l�k�NS���G���� }���O��K($d���?�J�m2�?@��l��t?:iL���m? O��V?��q�w? ��>o�=��kT�s?� ����r?���H�]?���n4b?�4�E?灕U�q?�(��e�=@��a}>8���K�>a`U}�|>Ĺ�$@�>�c���{>�������>����z�z>ը�=W��>�38z�j@ ��i�Φ0�0@@�'M%�C@��/��d�?   CLA-S02-MAG-QUAD-02      KQUAD�,>�t?����`�>���#�ܖ>��W/bI��ڝ� �Ǒ>x����گ����>��<_�e��o9?n�7m(c>��Ҿ��`���'�U>?��9�s��4~�q�<��l�e4[?W:�ɵ�s��D`�}>c��,8�����0U��<�<|��I?F+\�El���H��>#?�xN`���>���E?��*o�Ǿ)1�tE8�<灕U�q?�80�mw�@k�w1g�=;Tt���?QW�WL?�}���r?� .d? ��Z	�V?��G���? V.�o�=ǞgV��VO�1�G�nq�f�� .d� Z��MS���G���� �.z�O��;Tt���?QW�WL?�}���r?T�(�cXU? ��Z	�V?��q�w? V.�o�=�,>�t?_�e��o9?��l�e4[?�<|��I?�>���E?灕U�q?@k�w1g�=��a��>�\u��J�>1��>j�2rE�>eݱ)�2z>-�H��L�>t�ɧ�	z>��L0�>��
h�j@��x�2h0���xp<@Q|[Txt*@I�����?   DRIFT3      CSRDRIFT���4��t?8'Ȗ���>��
}�>�S��C���abn�>��Ky����p_g�<_�e��o9?D��,aIa>��Ҿ��`�v4jٰU>?��9�s���`�s�<h�}��Y?Ij��"���� ~Q(�{>�= BB��+v� �<�<|��I?�OAGfHl���H��>H��$'e����:��E?h]��c�Ǿ�t�	�:�<灕U�q?뒩5ry��V��h�=\"Z���?QW�WL?F��é�q?� .d? N����V?��G���? ���q�=iOʛ�:��VO�1�G�^�3Zpe�� .d� 6pMS���G���� �+�P��\"Z���?QW�WL?F��é�q?T�(�cXU? N����V?��q�w? ���q�=���4��t?_�e��o9?h�}��Y?�<|��I?��:��E?灕U�q?�V��h�=��a��>�\u��J�>0��>j�2rE�>�ܱ)�2z>��H��L�>ؓɧ�	z>E�L0�>���#k@�D᳚�0�(z-�/9@�3�)@I�����?   CLA-S02-DIA-SCR-01      WATCH���4��t?8'Ȗ���>��
}�>�S��C���abn�>��Ky����p_g�<_�e��o9?D��,aIa>��Ҿ��`�v4jٰU>?��9�s���`�s�<h�}��Y?Ij��"���� ~Q(�{>�= BB��+v� �<�<|��I?�OAGfHl���H��>H��$'e����:��E?h]��c�Ǿ�t�	�:�<灕U�q?뒩5ry��V��h�=\"Z���?QW�WL?F��é�q?� .d? N����V?��G���? ���q�=iOʛ�:��VO�1�G�^�3Zpe�� .d� 6pMS���G���� �+�P��\"Z���?QW�WL?F��é�q?T�(�cXU? N����V?��q�w? ���q�=���4��t?_�e��o9?h�}��Y?�<|��I?��:��E?灕U�q?�V��h�=��a��>�\u��J�>0��>j�2rE�>�ܱ)�2z>��H��L�>ؓɧ�	z>E�L0�>���#k@�D᳚�0�(z-�/9@�3�)@����)��?   DRIFT4      CSRDRIFTJn�Xu?��$���>^&M�F�>�ع�Iԗ�M�g2�#�>����>��Te@WQE�<_�e��o9?�PFa�]>��Ҿ��`�_�M'ıU>?��9�s�-$��u�<`����W?���o�����G�y>��`��f��Kh �C�<�<|��I?ĩ���Kl���H��>&�gp�k���TW��E?�+%T�Ǿ��	o�=�<灕U�q?��x�|��o@ak�=	��o�.�?QW�WL?(�tap?� .d? ����V?��G���? ���s�=$/�}�o��VO�1�G�����c�� .d� `|;MS���G���� �;��R��	��o�.�?QW�WL?(�tap?T�(�cXU? ����V?��q�w? ���s�=Jn�Xu?_�e��o9?`����W?�<|��I?�TW��E?灕U�q?�o@ak�=��a��>�[u��J�>1��>Yi�2rE�>�ܱ)�2z>��H��L�>ٓɧ�	z>E�L0�>�1����k@)���0��O*��5@��m0'@y"1��?   CLA-S02-MAG-HVCOR-02      KICKER��*uIu?f&�7���>\ 	�x��>^���G䗾��Q8.�>��;RH������O�<_�e��o9?�aNx��\>��Ҿ��`�23���U>?��9�s��U�� v�<�� ��{W?���*ʲ�͆�V-yy>0�̈�� ퟣn�<�<|��I?
��mLl���H��>��A��l��~��E?ˉ�Q�Ǿ��W�}>�<灕U�q?�ͮ��|��J���k�=����e<�?QW�WL?�tQ�Np?� .d? :�ے�V?��G���? *xt�=$��Wjz��VO�1�G��n�v�Jc�� .d� @��@MS���G���� ��R������e<�?QW�WL?�tQ�Np?T�(�cXU? :�ے�V?��q�w? *xt�=��*uIu?_�e��o9?�� ��{W?�<|��I?~��E?灕U�q?�J���k�=��a��>b]u��J�>2��>�j�2rE�>ݱ)�2z>��H��L�>$�ɧ�	z>z�L0�>4�ڡ��k@9p"_�0��3��4@Y�*�+�&@��|��?   DRIFT5      CSRDRIFT���8u?�H.��>ij���ݍ>Ђ������N@�H�>N�Y�_����qug�<_�e��o9?�*f�Z>��Ҿ��`����Jk�U>?��9�s��x�5w�<���E�V?��҉���⴨�hx>O��]J����F�<�<|��I?�$˧"Nl���H��>�'X:p���u���E?���2I�ǾwTs�@�<灕U�q?s7�� ~���J�m�=�]ﯧ^�?QW�WL?;����n?� .d? փt�V?��G���? ��fu�=�˝�y���VO�1�G�`��G �b�� .d� �|~OMS���G���� ���S���]ﯧ^�?QW�WL?;����n?T�(�cXU? փt�V?��q�w? ��fu�=���8u?_�e��o9?���E�V?�<|��I?�u���E?灕U�q?��J�m�=��a��>�[u��J�>1��>Yi�2rE�>ݱ)�2z>��H��L�>#�ɧ�	z>y�L0�>�p�G3l@�&Ru��0������;3@�T��%@v؜�'�?   CLA-S02-COL-01      ECOL�W�m�Os?1�`s��>���j8�>|P��k��g�B�Ta�>5�W|�Ⱦ�Iy�Jj�<@"��!7?�fO�m\>�(�td���7��e>���r���շP�Q�<2�R�BxR?��Щ6��H�ڣ6�r>���|�����_Ѕ�<e0	�LVJ?�~�8-l��]�f��>7�`][���>�1_�E?5�; �Ⱦφ9���<Ҟ��pr?M� ��B�מȵ�=5��EW�?���W�F?������g?� .d? l���W?���C�? x)
���=5��EW�����W�F����^^�� .d� �Q�S����C�� �m����y	!�?�E�ŖF?������g?T�(�cXU? l���W?sqR�}w? x)
���=�W�m�Os?@"��!7?2�R�BxR?e0	�LVJ?�>�1_�E?Ҟ��pr?B�מȵ�=��d��*t>�4?g-�>a�Ds�ds>YY<
��>*�n��{>lPP�b��>3OH���z>ת����>]�΀�r@%�k^Uw6�1\n��)@H3�N!�!@v؜�'�?   CLA-S02-APER-02      MAXAMP�W�m�Os?1�`s��>���j8�>|P��k��g�B�Ta�>5�W|�Ⱦ�Iy�Jj�<@"��!7?�fO�m\>�(�td���7��e>���r���շP�Q�<2�R�BxR?��Щ6��H�ڣ6�r>���|�����_Ѕ�<e0	�LVJ?�~�8-l��]�f��>7�`][���>�1_�E?5�; �Ⱦφ9���<Ҟ��pr?M� ��B�מȵ�=5��EW�?���W�F?������g?� .d? l���W?���C�? x)
���=5��EW�����W�F����^^�� .d� �Q�S����C�� �m����y	!�?�E�ŖF?������g?T�(�cXU? l���W?sqR�}w? x)
���=�W�m�Os?@"��!7?2�R�BxR?e0	�LVJ?�>�1_�E?Ҟ��pr?B�מȵ�=��d��*t>�4?g-�>a�Ds�ds>YY<
��>*�n��{>lPP�b��>3OH���z>ת����>]�΀�r@%�k^Uw6�1\n��)@H3�N!�!@�BY���?   DRIFT6      CSRDRIFTQ%Оm|s?B�S���>��?,�"�>��:k���p������>8/�?�Ⱦ)�E�<@"��!7?��Hf�pW>�(�td�!��;l�e>���r����!o��S�<ȕZ���P?��2 ������t
q>y��@	�����d���<e0	�LVJ?�w��(0l��]�f��>@t���`��<���W�E?����Ⱦo�^�� �<Ҟ��pr?�x��."�I�eƷ�=��t�僃?���W�F?�0��(e?� .d? �u�W?���C�? 8qP��=��t�僃����W�F��a��0\�� .d� 4�؝S����C�� �xe��=?�~M�?�E�ŖF?�0��(e?T�(�cXU? �u�W?sqR�}w? 8qP��=Q%Оm|s?@"��!7?ȕZ���P?e0	�LVJ?<���W�E?Ҟ��pr?I�eƷ�=��d��*t>�3?g-�>��Ds�ds>2X<
��>v�n��{>�PP�b��>~OH���z>8ת����>q���1s@���ح�6�Vd���$@���;�3 @W@ܕ�?   CLA-S02-MAG-HVCOR-03      KICKER��6�u�s?�;���>y��~�P�>I�AEϟ��~�~���>�׷�	�Ⱦ�֮�Q��<@"��!7?���~6V>�(�td������e>���r����%eNT�<����{P?+D���몾D�(�p>���MJQ���=е��<e0	�LVJ?� ���0l��]�f��>o�F�4b���oV�E?�g���ȾMӉ)n�<Ҟ��pr?�ѷ��"�3m�C��=e���?���W�F?䫎��d?� .d? d%�W?���C�? (ݹ���=e�������W�F�]]��n[�� .d� T��S����C�� p�Թ���9�W�?�E�ŖF?䫎��d?T�(�cXU? d%�W?sqR�}w? (ݹ���=��6�u�s?@"��!7?����{P?e0	�LVJ?�oV�E?Ҟ��pr?3m�C��=��d��*t>�4?g-�>\�Ds�ds>RY<
��>v�n��{>�PP�b��>~OH���z>8ת����>_"Z�ZGs@�j����6�N��?��#@ ���@��g�:�?   DRIFT7      CSRDRIFT_�l�:�s?��i�Qd�>��O��>�[���Q��,Cϣ>��ԪWɾO�L����<@"��!7?ۜP�>�N>�(�td�I�)E��e>���r�������V�<����L?��kV����R�l>����7��9^y�é<e0	�LVJ?mo��4l��]�f��>[��i���[CL�E?M/s �ȾYd(�<Ҟ��pr?����%��������=����[˃?���W�F?���Ã<a?� .d? �LpW?���C�? H�~��=����[˃����W�F��}�e�=X�� .d� |��S����C�� @̓�!���z𷮓�?�E�ŖF?���Ã<a?T�(�cXU? �LpW?sqR�}w? H�~��=_�l�:�s?@"��!7?����L?e0	�LVJ?�[CL�E?Ҟ��pr?�������=��d��*t>s0?g-�>�Ds�ds>�T<
��>v�n��{>�PP�b��>~OH���z>8ת����>�9p@�s@��>ڀ�6�7���h*@����m@��g�:�?   CLA-S02-DIA-SCR-02      WATCH_�l�:�s?��i�Qd�>��O��>�[���Q��,Cϣ>��ԪWɾO�L����<@"��!7?ۜP�>�N>�(�td�I�)E��e>���r�������V�<����L?��kV����R�l>����7��9^y�é<e0	�LVJ?mo��4l��]�f��>[��i���[CL�E?M/s �ȾYd(�<Ҟ��pr?����%��������=����[˃?���W�F?���Ã<a?� .d? �LpW?���C�? H�~��=����[˃����W�F��}�e�=X�� .d� |��S����C�� @̓�!���z𷮓�?�E�ŖF?���Ã<a?T�(�cXU? �LpW?sqR�}w? H�~��=_�l�:�s?@"��!7?����L?e0	�LVJ?�[CL�E?Ҟ��pr?�������=��d��*t>s0?g-�>�Ds�ds>�T<
��>v�n��{>�PP�b��>~OH���z>8ת����>�9p@�s@��>ڀ�6�7���h*@����m@a_y����?   DRIFT8      CSRDRIFT�^JBt?4K �&��>��)�}3q>��.��S��_�?���>�q��Wɾ�_Z{Z�<@"��!7?���RA>�(�td�q��x�e>���r���6���Y�<����UH?!�*m����8�#��g>W�GݍԖ� &C�3��<e0	�LVJ?�혚�8l��]�f��>�l6|q�����cB�E?�y�/�Ⱦ�$��<Ҟ��pr?ܝ!��(���񦬽�=*N@��?���W�F?�ڈ�L\?� .d? d�*,W?���C�? 81�`��=*N@������W�F���t�`	U�� .d� 8m��S����C�� @�J]#���m���σ?�E�ŖF?�ڈ�L\?T�(�cXU? d�*,W?sqR�}w? 81�`��=�^JBt?@"��!7?����UH?e0	�LVJ?���cB�E?Ҟ��pr?��񦬽�=��d��*t>�3?g-�>��Ds�ds>9X<
��>c�n��{>�PP�b��>jOH���z>*ת����>Fn�";t@>���F7� bb�1�@�ӪR�3@��*�?   CLA-S02-MAG-QUAD-03      KQUAD�����r?�ݎ�� ���we:,S>�}p�-���"$�ɛ�>�)��ǾQh�w��<��$��}?��@��]����0s�>H3:E��� Q(W7s�>ItNV�4�3!�]�G?����W-�>U� 
�f>����������
X��<���7?�I�<ͬN>��s���b��Z��<kgo��E?�r����ȾW���<Ҟ��pr?p�, )�y�@ν�=w盆ퟂ?�:��?���|G[?g���I? �����V?���C�? ���-��=w盆ퟂ��Z�|�����"6�T�g���I� �L�S����C�� �=����*"x@?k�?�:��?���|G[?k.sGD�G? �����V?sqR�}w? ���-��=�����r?��$��}?3!�]�G?���7?kgo��E?Ҟ��pr?y�@ν�=r�m(MՅ>��U�-��>7 ���r�>��P����>�C���z>ߚG���>9�ʭz>��,��>�	���_@�&6��h@`M���@0W��[:���o{��@   DRIFT9      CSRDRIFT�7����c?`1��A��A�ji@l���3�ߋ����J��>K<��j���ef��<��$��}?!�M��>���0s�>1��I� �� Q(W7s�>��\�����s�J?��9�ђ>�a�3m�h>eO�%	���TQOr�<���7?�#�N>��s��L� �S>�<"WL�E?��h�׃Ⱦy�(����<Ҟ��pr?L���i��.��贃=v����s?�:��?��Ĉb�^?g���I? X{gL�V?���C�? M����=v����s��Z�|���S�O�X�g���I� �u�t�R����C�� ����H��s?�:��?��Ĉb�^?k.sGD�G? X{gL�V?sqR�}w? M����=�7����c?��$��}?���s�J?���7?"WL�E?Ҟ��pr?�.��贃=�Ym(MՅ>.�U�-��>�����r�>4�P����>�C���z>ߚG���>9�ʭz>��,��>��1x=�A@&���KZ@����@;���_�=��H�r@   CLA-S02-MAG-QUAD-04      KQUAD��5�|`?.C�D�Dľ���	7m���L>�d��W�>��;M\���ek3�np�<>y�2�S?A1��rc>��,$�P>�9�[������+�>Pq��/W¼gg��MdH?��B �߶���V��9f>��$*�������<����O^?R��4�|��W#��>S���>��� �E?��y�Ⱦ�dEr��<Ҟ��pr?�wZ&1�C�K�д�=#G�"t�p?sNw>�c?�V E��[?�3��uq? �_�
�V?���C�? `S����=#G�"t�p�V{<h�]c��N�s|V��3��uq� �z�R����C�� �J-��w�EZZp?sNw>�c?�V E��[?��?'Ej? �_�
�V?sqR�}w? `S����=��5�|`?>y�2�S?gg��MdH?����O^?>��� �E?Ҟ��pr?C�K�д�=J�U��>�e�?�&�>�G5��2�>��6���>��.8dT{>�G���>�|dI,{>������>%�-�t@@��[aq�3@m�Pç�@�+�7�*@S��D�%@   DRIFT10      CSRDRIFT�m���R?$�Z2�C��S�ݯ�i��
з]�e»B�6�>u�J��Ϧ�6��#ho�<>y�2�S?/m,gi>��,$�P>��e������+�>�S��h¼�I�1�B?)�$,(r�>��� �b�E��+���>5��V�*������O^?��l}�|��W#��>���2=��9�G��E?k�q:w~ȾS��ʳ��<Ҟ��pr?t"ˉ�(�qGd���=."�,/4c?sNw>�c?�ף�,Y?�3��uq? ����V?���C�? 0����=."�,/4c�V{<h�]c��ף�,Y��3��uq� ��'�R����C�� @����Fe�e�b?sNw>�c?R�-pp�M?��?'Ej? ����V?sqR�}w? 0����=�m���R?>y�2�S?�I�1�B?����O^?9�G��E?Ҟ��pr?qGd���=�I�U��>Ge�?�&�>_G5��2�>Q�6���>��.8dT{>bG���>�|dI,{>_�����>V��Bw�%@�侄4�&@V���1K	@<� OR$��{+�@   CLA-S02-MAG-QUAD-05      KQUAD ����S?#��x���>��:��h��P'�>�R��s�>��/�����Z'�<Q��,Yd?�i��z�<�0����>��c;B�>|�u�憶�iI]dUz�<&��VR~E?�1�y�ǙC��e� Y�'�^�>_����wyr{,?���[�oM>7��PMu�q�晊<��l���E?��3~Ⱦ��q�B��<Ҟ��pr?��V�*�-�@��=���g?d?�@ct? ��
��[?�\X���Q? �S�V�V?���C�? �
�$��=���g?d��@ct� ��
��[�4K���7�  Z�R����C�� `̬���*���L�c?��e�s?�eM�Q?�\X���Q? �S�V�V?sqR�}w? �
�$��= ����S?Q��,Yd?&��VR~E?wyr{,?��l���E?Ҟ��pr?-�@��=R����.~>�C��>��D�0k}>,a�(��>�i���{>,�e~d�>�^��X�{>2í�mH�>��A���*@���ό�:�#�Cu�@D�KVG�?��B=]	@   CLA-S02-DIA-BPM-02      MONI ����V?���y��>c�
M��g�^����>m}d����>�f���Spx���<Q��,Yd?#����v�<�0����>WŬA�>|�u�憶��2e\z�<�}�&@E?��k��x���a/e�I��'��>�>$��3��wyr{,?c(�nM>7��PMu�1(J����<q=,�.�E?�}�}Ⱦ�1�O��<Ҟ��pr?����*�+��x��=(��kWf?�@ct?櫓�k�Z?�\X���Q? Ȱ��V?���C�? ��8���=(��kWf��@ct�櫓�k�Z�4K���7� �O�R����C�� �.$��)��R��e?��e�s?r�y��Q?�\X���Q? Ȱ��V?sqR�}w? ��8���= ����V?Q��,Yd?�}�&@E?wyr{,?q=,�.�E?Ҟ��pr?+��x��=R����.~>�C��>��D�0k}>0a�(��>�i���{>,�e~d�>�^��X�{>2í�mH�>q�l\�50@��9�u=��Z�Ep.@Z��V��? D���	@   DRIFT11      CSRDRIFT��~y�W?Y��C��>�+�^�f����N�>jл�c�>�1�h�꫾�BH476�<Q��,Yd?�C�e��s�<�0����>���9A�>|�u�憶�d	�bz�<�D2&�E?-}.��px���3s�d�k` 5G��>U��i�좼wyr{,?��M׋mM>7��PMu��r���<�J��E?{��� }Ⱦ�:�Z��<Ҟ��pr?����a+�����=�Q��h?�@ct?x����Y?�\X���Q? @A+�V?���C�? �r�֬�=�Q��h��@ct�x����Y�4K���7� 8��&�R����C�� ���������[�g?��e�s?Dj�|�Q?�\X���Q? @A+�V?sqR�}w? �r�֬�=��~y�W?Q��,Yd?�D2&�E?wyr{,?�J��E?Ҟ��pr?����=R����.~>�C��>��D�0k}>:a�(��>�i���{>,�e~d�>�^��X�{>2í�mH�>B�h��2@e�V���?��cآ�@&������? D���	@   CLA-S02-DIA-SCR-03      WATCH��~y�W?Y��C��>�+�^�f����N�>jл�c�>�1�h�꫾�BH476�<Q��,Yd?�C�e��s�<�0����>���9A�>|�u�憶�d	�bz�<�D2&�E?-}.��px���3s�d�k` 5G��>U��i�좼wyr{,?��M׋mM>7��PMu��r���<�J��E?{��� }Ⱦ�:�Z��<Ҟ��pr?����a+�����=�Q��h?�@ct?x����Y?�\X���Q? @A+�V?���C�? �r�֬�=�Q��h��@ct�x����Y�4K���7� 8��&�R����C�� ���������[�g?��e�s?Dj�|�Q?�\X���Q? @A+�V?sqR�}w? �r�֬�=��~y�W?Q��,Yd?�D2&�E?wyr{,?�J��E?Ҟ��pr?����=R����.~>�C��>��D�0k}>:a�(��>�i���{>,�e~d�>�^��X�{>2í�mH�>B�h��2@e�V���?��cآ�@&������? D���	@   END      WATCH��~y�W?Y��C��>�+�^�f����N�>jл�c�>�1�h�꫾�BH476�<Q��,Yd?�C�e��s�<�0����>���9A�>|�u�憶�d	�bz�<�D2&�E?-}.��px���3s�d�k` 5G��>U��i�좼wyr{,?��M׋mM>7��PMu��r���<�J��E?{��� }Ⱦ�:�Z��<Ҟ��pr?����a+�����=�Q��h?�@ct?x����Y?�\X���Q? @A+�V?���C�? �r�֬�=�Q��h��@ct�x����Y�4K���7� 8��&�R����C�� ���������[�g?��e�s?Dj�|�Q?�\X���Q? @A+�V?sqR�}w? �r�֬�=��~y�W?Q��,Yd?�D2&�E?wyr{,?�J��E?Ҟ��pr?����=R����.~>�C��>��D�0k}>:a�(��>�i���{>,�e~d�>�^��X�{>2í�mH�>B�h��2@e�V���?��cآ�@&������?