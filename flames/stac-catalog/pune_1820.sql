PGDMP         $    
            |            Flame_db_13july    12.18    12.18     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16393    Flame_db_13july    DATABASE     �   CREATE DATABASE "Flame_db_13july" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_India.1252' LC_CTYPE = 'English_India.1252';
 !   DROP DATABASE "Flame_db_13july";
                postgres    false                       1259    18497 	   Pune-1820    TABLE     �   CREATE TABLE public."Pune-1820" (
    id integer NOT NULL,
    geom public.geometry(Geometry,4326),
    shape_file_name text
);
    DROP TABLE public."Pune-1820";
       public         heap    postgres    false                       1259    18495    Pune-1820_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Pune-1820_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."Pune-1820_id_seq";
       public          postgres    false    279            �           0    0    Pune-1820_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."Pune-1820_id_seq" OWNED BY public."Pune-1820".id;
          public          postgres    false    278                       2604    18500    Pune-1820 id    DEFAULT     p   ALTER TABLE ONLY public."Pune-1820" ALTER COLUMN id SET DEFAULT nextval('public."Pune-1820_id_seq"'::regclass);
 =   ALTER TABLE public."Pune-1820" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    279    278    279            �          0    18497 	   Pune-1820 
   TABLE DATA           @   COPY public."Pune-1820" (id, geom, shape_file_name) FROM stdin;
    public          postgres    false    279   �
       �           0    0    Pune-1820_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public."Pune-1820_id_seq"', 1, true);
          public          postgres    false    278                       2606    18505    Pune-1820 Pune-1820_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public."Pune-1820"
    ADD CONSTRAINT "Pune-1820_pkey" PRIMARY KEY (id);
 F   ALTER TABLE ONLY public."Pune-1820" DROP CONSTRAINT "Pune-1820_pkey";
       public            postgres    false    279            �   �  x�}�;�%7E��x@R?2�H)��pd0��j�u�ИJ
�S���$� �Bx�Vg�|�K���sWV�;��0�Qv�8��]#<x>|hZ��g��?ҕ��
/�,�y����5{�}xk��%+.�z�\"�dى���+IQ�5���7����YW|���K��5.]q8ќ��]M�;���D�W���gG���B�g�^R�>�9y�'�wN��H:����
��7�*�<���'��ڹ�N�·3��F�Y���zJɇo*>��ɯi�]ܤ�?��ë��$۵��_G�X�O�����2�����tM�O}8��fXıw�)��ӟ���F���ޥ?<iq�6�c>�S�&��^ފ��/��ZW�Ro���a�ųgF�ՏЀ���r�S�R*?��"��Cl3y�QQh-������	�X�n}�Ƀ@R.�/��L`_���-��>?hW�M�\{#e�J��u8����r�ê��r�lQW�W?��6��/>���۾�F�T�������h��˕�Ԍ���ּ��Aӥ��/�����/>f5z�����{H�Ǐ�3��^���Ɩ����d_~��~�Q� ���=F�ڂ���؇<��/�#���s?��������Z�����&Q<�5߿޿?~���?c���_�|��������H�     