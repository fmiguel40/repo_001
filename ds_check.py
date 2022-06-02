
import pandas as pd
from pandas.core.common import flatten

#Setting to display Dataframe by maximizing column width
pd.set_option('display.max_colwidth', None)

#Display all columns
pd.set_option('display.max_columns', None)

#https://stackoverflow.com/questions/64420348/ignore-userwarning-from-openpyxl-using-pandas
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

#https://towardsdatascience.com/8-commonly-used-pandas-display-options-you-should-know-a832365efa95
#Esta opção limita os floats em 2 casas decimais.
pd.set_option('display.precision', 2)

#PARA TESTAR OS TIPOS DE DADOS NAS COLUNAS.
#https://stackoverflow.com/questions/22697773/how-to-check-the-dtype-of-a-column-in-python-pandas
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_float_dtype
from pandas.api.types import is_datetime64_any_dtype

from dateutil.parser import parse #--> CHECK DATE FORMAT

#from utils.dataframes_pandas import count, ds_convert, ds_find
from utils.dataframes_pandas import ds_count, ds_convert, ds_find


######################################################################################
def if_all_col_values_are_upper (df, col_name):

    """
    Esta função verifica se todos os elems de uma coluna são strings maiúsculas.


    :param df:
    :param col_name:
    :return: bool
    """

    lst_resultados = [True for col_elem in df[col_name] if isinstance(col_elem, str) and col_elem.isupper()]

    # Eliminando duplicidades.
    lst_resultados = list(set(lst_resultados))  # Retorna uma lista cheia de "True" ou uma lista vazia.

    # Retorna "True" se a lista tiver apenas um elemento e se este elemento for o boolean "True".
    # Caso contrário, retornará "False"
    return True if len(lst_resultados) == 1 and lst_resultados[0] == True else False

######################################################################################
def if_dfs_have_same_col_headers (df1, df2):

    """
    Esta função verifica se dois dfs possuem os mesmos headers.

    :param df1:
    :param df2:
    :return: bool
    """

    df1_lst_col_names = ds_convert.column_names_to_list(df1)
    df2_lst_col_names = ds_convert.column_names_to_list(df2)

    if df1_lst_col_names == df2_lst_col_names:
        return True
    else:
        return False


######################################################################################
def if_all_headers_are_strings (df):

    """
    Esta função verifica se todos os nomes de coluna (headers) são do tipo string.

    :param df:
    :return: bool
    """

    qtd_colunas = ds_count.columns(df)

    # Contador do núm de headers do tipo string.
    counter_headers_str_format = 0

    for col_name in df:
        if isinstance(col_name, str):
            counter_headers_str_format += 1

    # Se o número de nomes de colunas que sejam do tipo string for igual à "qtd_colunas",
    # então, todos os headers são do tipo string.
    if qtd_colunas == counter_headers_str_format:
        return True
    else:
        return False

######################################################################################
def if_two_values_are_on_same_row (df, col_name_01, col_name_02, value_col_01, value_col_02):
    """
    Este método descobre se dois valores em colunas DIFERENTES estão na mesma linha.

    Parameters:
        -> df (dataframe)
        -> col_name_01 (str) ---> nome da coluna na qual o "value_col_01" será buscado;
        -> col_name_02 (str) ---> nome da coluna na qual o "value_col_02" será buscado;
        -> value_col_01 (str) ---> valor a ser buscado na primeira coluna (col_name_01);
        -> value_col_02 (str) ---> valor a ser buscado na segunda coluna (col_name_02).

    Return:
        -> True/False (bool)
    """

    col_name_01 = str(col_name_01)
    col_name_02 = str(col_name_02)
    value_col_01 = str(value_col_01)
    value_col_02 = str(value_col_02)

    df_temp = df[(df[col_name_01] == value_col_01) & (df[col_name_02] == value_col_02)]

    row_index_value_col_01 = ds_find.rowIndex_by_keyword(df_temp, value_col_01)
    row_index_value_col_02 = ds_find.rowIndex_by_keyword(df_temp, value_col_02)

    return True if row_index_value_col_01 == row_index_value_col_02 else False

####################################################################################
def nan_in_column (df, col_name):
    """
    Esta função verifica se determinada coluna possui NaNs.

    Parameters -> df, col_name
    Return -> bool

    https://datatofish.com/check-nan-pandas-dataframe/
    https://stackoverflow.com/questions/47440077/checking-if-particular-value-in-cell-is-nan-in-pandas-dataframe-not-working-us

    """

    return df[col_name].isnull().values.any()

####################################################################################
def nan_in_all_dataframe (df):

    """
    Esta função verifica se existem NaNs no dataframe.

    Parameters -> df
    Return -> bool

    https://datatofish.com/check-nan-pandas-dataframe/
    https://stackoverflow.com/questions/47440077/checking-if-particular-value-in-cell-is-nan-in-pandas-dataframe-not-working-us

    """

    return df.isnull().values.any()

####################################################################################
def is_dataframe(df):

    """
    :param df:
    :return: bool
    """

    return isinstance(df, pd.DataFrame)

####################################################################################
def is_date (string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """

    # Conversão float -> string.
    string = str(string)

    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

######################################################################################
def has_centavos (valor):
    """
    Esta função verifica se um valor de moeda possui separador de centavos.


    Parameter: valor -> float
    """

    # Verificando se "valor" possui formato de data. Se for o caso -> return False.
    if is_date(valor):  # True/False
        return False

    if isinstance(valor, str):
        valor = float(valor)

    # Limitando o float em duas casas decimais.
    valor = round(valor, 2)
    # Conversão float -> string.
    valor = str(valor)

    # Achar o index do último ponto separador no número.
    last_period_index = valor.rds_find('.')

    # Index do último caracter.
    last_char_index = len(valor) - 1

    # Se houver separador de centavos, a diferença entre a posição (index) do último caracter e a posição do último ponto deve ser igual a 2.
    diferenca = last_char_index - last_period_index

    # return True if diferenca == 2 else False
    if diferenca == 2:
        return True
    else:
        return False

######################################################################################
def if_col_value_is_string(df, col_name):

    """
    Esta função verifica se o(s) elementos(s) de uma colunas é(são) do tipo string.

    :param df:
    :param col_name:
    :return: bool
    """

    return is_string_dtype(df[col_name])

######################################################################################
def if_col_value_is_numeric (df, col_name):

    """
    Esta função verifica se o(s) elementos(s) de uma coluna é (são) do tipo numeric.

    :param df:
    :param col_name:
    :return: bool
    """

    return is_numeric_dtype(df[col_name])

######################################################################################
def if_col_value_is_float (df, col_name):

    """
    Esta função verifica se o(s) elementos(s) de uma coluna é (são) do tipo float.

    :param df:
    :param col_name:
    :return: bool
    """

    return is_float_dtype(df[col_name])

######################################################################################
def if_any_column_has_float (df):

    """
    Esta função percorre todos os elementos de df e verifica se pelo menos um está no formato float.

    :param df:
    :return: bool
    """

    for col_name in df.columns:
        elem_col = df[col_name][0]

        if isinstance(elem_col, float):
            return True
    return False

######################################################################################
def if_value_is_float(value):

    """
    Esta função verifica se o valor recebido é do tipo float.

    :param value:
    :return: bool
    """

    return isinstance(value, float)


######################################################################################
def if_value_is_string (value):
    """
    Esta função verifica se o valor recebido é do tipo string.

    :param value:
    :return: bool
    """

    return isinstance(value, str)

######################################################################################
def if_value_is_integer (value):
    """
    Esta função verifica se o valor recebido é do tipo integer.

    :param value:
    :return: bool
    """

    return isinstance(value, int)

######################################################################################
def if_has_numbers (value):

    """
    Esta função verifica se 'value', independente do seu tipo, contém números.

    :param value:
    :return: bool
    """

    # A linha a seguir é necessária porque objetos do tipo 'numpy.float64' não são iteráveis.
    if isinstance(value, float) and value is not None:
        value = str(value)

    return any(char.isdigit() for char in value)

######################################################################################
def if_df_is_empty(df):

    """

    :param df:
    :return: bool
    """

    return df.empty

