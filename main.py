
#############################################
# PROJE: KURAL TABANLI SINIFLANDIRMA
#############################################

# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None)
df = pd.read_csv('persona.csv')
df.head()
df.tail()
df.shape #kaç satır kaç sütun
df.columns#df sütunlarının ve veri tiplerinin ne olduğunu öğrenelim
df.index
df.describe().T #sayısal değişkenleri betimleme
df.isnull().any()#eksik değer var mı yok mu sorusu
df.isnull().sum()#veri setindeki bütün değerlerdeki eksik değer sayısını veren fonksiyon
df.info()
# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].unique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# Soru 7: SOURCE türlerine göre  satış sayıları nedir?
df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby('COUNTRY').agg({"PRICE": "mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})




#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################


df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).head(50)


#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################

# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.



agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df.head()
agg_df.columns


#############################################
# GÖREV 4: Index'te yer alan isimleri değişken ismine çeviriniz.
#############################################

# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()

agg_df.reset_index(inplace=True) #reset_index() --> indexteki değerleri sütuna çevirir
#2.yol --> agg_df=agg_df.reset_index()
print(agg_df.head())

#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################

# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

############################################################## 1.yol
agg_df["AGE_CAT"]=pd.cut(agg_df["AGE"],[0,18,23,30,40,70])
agg_df
agg_df["AGE_CAT"]=agg_df["AGE_CAT"].astype(str)
agg_df["AGE_CAT"].value_counts()

agg_df.loc[agg_df["AGE_CAT"]=="(0, 18]","AGE_CAT"]="0_18"
agg_df.loc[agg_df["AGE_CAT"]=="(18, 23]","AGE_CAT"]="19_23"
agg_df.loc[agg_df["AGE_CAT"]=="(23, 30]","AGE_CAT"]="24_30"
agg_df.loc[agg_df["AGE_CAT"]=="(30, 40]","AGE_CAT"]="31_40"
agg_df.loc[agg_df["AGE_CAT"]=="(40, 70]","AGE_CAT"]="41_70"
print(agg_df.head())
print(agg_df["AGE_CAT"].dtype)


############################################################## 2.yol
#bins=[0,18,23,30,40,70]
#mylabels= ['0_18', '19_23', '24_30', '31_40', '41_70']
#agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins,labels=mylabels)
#print(agg_df.head())
###############################################################



####GÖREV6####
#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
#Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
#Yeni eklenecek değişkenin adı: customers_level_based
#Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir.

print("GÖREV 6")

agg_df["customer_level_based"]=agg_df["COUNTRY"]+("_")+agg_df["SOURCE"]+("_")+agg_df["SEX"]+("_")+agg_df["AGE_CAT"]
agg_df["customer_level_based"]=agg_df["customer_level_based"].str.upper()
delete_columns=["COUNTRY","SOURCE","SEX","AGE_CAT","AGE"]
agg_df.drop(delete_columns,axis=1,inplace=True)
agg_df1=agg_df.groupby("customer_level_based").agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False).reset_index()
print("------------")
print(agg_df1)
print("-------------")

##GÖREV7###
#Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve
#ne kadar gelir getirebileceğini tahmin ediniz.

#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve
#ortalama ne kadar gelir kazandırması beklenir?

#35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne
#kadar gelir kazandırması beklenir?

def check_df(dataframe,head=5):
    print("---------C segmentinin betimlenmesi----------")
    print("########## SHAPE ##########")
    print(dataframe.shape)
    print("########## TYPES ##########")
    print(dataframe.dtypes)
    print("########## HEAD ##########")
    print(dataframe.head(head))
    print("########## TAIL ##########")
    print(dataframe.tail(head))
    print("########## NA VALUES ##########")
    print(dataframe.isnull().sum())
    print("########## QUANTILES ##########")
    print(dataframe.describe(np.arange(0,1.05,0.05)).T)
    print("---------C segmentinin betimlenmesi----------")

check_df(df)




print("GÖREV 7")
#Yeni müşterileri (personaları) segmentlere ayırınız.

#Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.

#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.

#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

#C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz)


agg_df1["SEGMENT"] = pd.qcut(agg_df1["PRICE"], 4, labels=["A","B","C","D"])
agg_df1.groupby("SEGMENT").agg({"PRICE":["mean","max","min","sum"]})
a=agg_df1.loc[agg_df1["SEGMENT"]=="C"]
check_df(a) #betimleme amacıyla
print("GÖREV 7")
print(agg_df1.head())
agg_df1


print("GÖREV 8")
#Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz.
#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
#35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_user="TUR_ANDROID_FEMALE_31_40"
print("TR")
print(agg_df1[agg_df1["customer_level_based"]==new_user]) #customer_level_based sütununda new_user'a denk olan varsa yeni bir dataframe oluştur --> iç içe agg_df1 yazılması
new_user1="FRA_IOS_FEMALE_31_40"
print("FR")
print(agg_df1[agg_df1["customer_level_based"]==new_user1])

