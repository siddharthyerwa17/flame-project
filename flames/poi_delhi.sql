PGDMP     -    &    
             |            Flame_db_13july    12.15    12.15     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    19153    Flame_db_13july    DATABASE     �   CREATE DATABASE "Flame_db_13july" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_India.1252' LC_CTYPE = 'English_India.1252';
 !   DROP DATABASE "Flame_db_13july";
                postgres    false            �            1259    20500 	   poi_delhi    TABLE     �   CREATE TABLE public.poi_delhi (
    gid integer NOT NULL,
    id integer,
    point_of_i character varying(50),
    geom public.geometry(Point,4326)
);
    DROP TABLE public.poi_delhi;
       public         heap    postgres    false            �            1259    20498    poi_delhi_gid_seq    SEQUENCE     �   CREATE SEQUENCE public.poi_delhi_gid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.poi_delhi_gid_seq;
       public          postgres    false    236            �           0    0    poi_delhi_gid_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.poi_delhi_gid_seq OWNED BY public.poi_delhi.gid;
          public          postgres    false    235                       2604    20503    poi_delhi gid    DEFAULT     n   ALTER TABLE ONLY public.poi_delhi ALTER COLUMN gid SET DEFAULT nextval('public.poi_delhi_gid_seq'::regclass);
 <   ALTER TABLE public.poi_delhi ALTER COLUMN gid DROP DEFAULT;
       public          postgres    false    236    235    236            �          0    20500 	   poi_delhi 
   TABLE DATA           >   COPY public.poi_delhi (gid, id, point_of_i, geom) FROM stdin;
    public          postgres    false    236   �       �           0    0    poi_delhi_gid_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.poi_delhi_gid_seq', 83, true);
          public          postgres    false    235                       2606    20505    poi_delhi poi_delhi_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.poi_delhi
    ADD CONSTRAINT poi_delhi_pkey PRIMARY KEY (gid);
 B   ALTER TABLE ONLY public.poi_delhi DROP CONSTRAINT poi_delhi_pkey;
       public            postgres    false    236                       1259    20509    poi_delhi_geom_idx    INDEX     G   CREATE INDEX poi_delhi_geom_idx ON public.poi_delhi USING gist (geom);
 &   DROP INDEX public.poi_delhi_geom_idx;
       public            postgres    false    236            �   0	  x���Ks�H��ů���,���c�O�1v�����&m˔pUɣ���_?GR�=�@ e}q�>�=)����ñl��[�o�o�b$��	Jx���Yd�I<o���YyÀ�w97���^ ��6>;2<�Y9'rtj$p>��n{[�O �%�6J-E <p�X$�;1 7�p�2)���9?=*,2��C�o�SB9��E+=w�ډ⭰<2'H́ڰ�����$�h�K)"��0A���1�"q~�h@�u������ �<3LQWӡ�d�["U�>��ݡ�/��}8��K�8̈́#�+*�مg��i�w����9��$}Ҧr��22jRpn�PП��9��p�7�$KL��J�Y+�w�L
L,�����WN�2^SD4�]��EI�}GH��y� ���_j���l���3�����7|����.�����{�%w��L��p@��H��xD�6ĳ �!�QE7�=X!�Ht�H@���?m���/�oWe_�5��/��LR�|��wJR�8uNNH���8�	I
�K�[J�F[���GԔ%Ǡs�5P��wh�v=UQ�������j��#���߀��m@(�Y�V&�v1c;V�� �	&�a�X}\��%��5�DP��ML�����=��&zI6����6��:{����bt#7חù�D6v��#1.gbk�q�z��a��T�_VA����`�e��gFp�q�+�UD ��d�E�2 ��	@��{9���>����E�!�P����ɠ���8�uwnW��S����R�H/�Q��}�Q�[_�N�mJc�x�Љ�L�*�����#]�����?/����U݉Λ����%�Hn��� !ǲ��q!�Wq�`�aVc7��X�2���'<�4MŅ�6��+���ɚC��o?��}Y��k嘍:U�Sm����ʇf��r�}_�	Ú��XRw�"<
��Ԝp����w�Q@Њ2��T)#l|	��캾YcX���9�z��������0B��_��F�\í���Nf�8����O�gW�k杠(���f��4$i�|���G_ΫI�:��?�����j4׿�k�hO-��i���"!T����	�a5h��JB���l�w�A''��}=4�z C=���:�L���@��Y#���v�ܬ�bD��T�5�1AA�kj�e�x�ω�ڱDj*>��*b�ثrwٯ!�Š��A�C���Hij���c����x�ȃ��8$�%�4�M!� N�C�Nq�coA�R�xd�h_(C�^5��W;��~�J��(�:ř3H���^����n��ݒ��bi�B5 ��� ,��z��s{�Z�n��yx5g�"���[�,&n�Aiå�	k����s�I�j�N��m5�������p:/�/\"�1��y}`$���� ��o�֏<���"���NB�Z8͚g9�����o?t_�%A�1���(����8�Y�$����M�x��P�`5�/�;*�|���c4X���M_�E�r��2��2nu�e0	��gt̒C��E���3g)���!���z���z9���au��4B��S���jUr�d�a�14L�/7��%����3'�HV�A��|�N�m����/J��B�x� ����� �����-�fi���<���k/A���ٺIn�h���hL0O>�jf�&J38��(��q��/����X�yT&��0��@7S6w�z����``r��xǜMx��be䴘��o�N�W�1@�Ar+������6t��+Gʎ�i���3�=~J�<�J����	���ˢ)e5�"���0*G4{�H`B����ˊ�J:e���B�&5(��n@)P��2L�ҟ�~i�r4�[�|m��T6Z�=��_���0A)hM��D+��z��1���V�$EF�q��:hbл� �At?�}{���o�.��tM͒�Ȭx�����0�tEi2�}�@~����s��)̓�m����nO�v\$����r��RE����X�6��*�/���A�� �&r�s]�!"Sg%u�5��n�0�0yߝ���G������-:�DReS`Bs�\c�(aD`��1���t~5%Q+�_]�S��i�o�*5��̙Q��?��6	�i\Q��c�p(1:I������Ij�1��eӑJY�{e0��f�z1���d������l�J��J���n�\�(�2��� rgs�s$���]_�۸�����8�R�q�������e�f�����iq�&�btȬ/ҳ�d�Lϯ� z�"�H�Y�{���9��d�[7�˷f���c9�q�W�I�Ȣ�\�=�p��kR��?o߼y�?�S3�     