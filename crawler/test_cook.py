from bs4 import BeautifulSoup


tmp = '''<div class="recipe-details"><meta content="Rea手绘食谱" itemprop="author"/><meta content="法式苹果克拉芙缇-手绘食谱 by Rea手绘食谱" itemprop="name"/>
<div class="recipe-details-header recipe-details-block">
<div class="header-row center-row">
<div class="header-col left-col">
<div class="recipe-cover"><a class="strip" data-strip-caption="法式苹果克拉芙缇-手绘食谱" data-strip-group="recipe-imgs" href="http://pih1wob2b.bkt.clouddn.com/icook_1542772820_0.jpg"><img alt="法式苹果克拉芙缇-手绘食谱" class="main-pic" itemprop="image" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772820_0.jpg" /> </a></div>
</div>
</div>

<div class="header-row description" itemprop="description">
<p>有着美丽名字的法式家常甜点克拉芙缇，融合布丁和蛋糕的口感，食材和做法原来这么简单，从备料到出炉45分钟完成，冷热都好吃，配上冰淇淋也很讚！是所有女生都该收藏并且做上一遍的超简单食谱~</p>

<p>想看更多的手绘食谱，请到脸书专页「Rea手绘本」<br />
<a href="https://www.facebook.com/ReaWatercolor/" rel="nofollow" target="_blank">https://www.facebook.com/ReaWatercolor/</a></p>
</div>
</div>

<div class="recipe-details-main">
<div class="recipe-details-info recipe-details-block">
<div class="servings-info info-block">
<div class="info-tag">份量</div>

<div class="info-content">
<div class="servings" itemprop="recipeYield"><span class="num">2</span> <span class="unit">人份</span></div>
</div>
</div>

<div class="time-info info-block">
<div class="info-tag">时间</div>

<div class="info-content"><meta content="PT45M" itemprop="totalTime"/><span class="num">45</span> <span class="unit">分钟</span></div>
</div>
</div>

<div class="recipe-details-ingredients recipe-details-block">
<div class="title">食材</div>

<div class="ingredients-groups">
<div class="group group-0">
<div class="ingredients">
<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">大苹果</div>

<div class="ingredient-unit">1颗</div>
<meta content="大苹果1颗" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">奶油</div>

<div class="ingredient-unit">10克</div>
<meta content="奶油10克" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">三温糖(红糖、蔗糖亦可)</div>

<div class="ingredient-unit">10克</div>
<meta content="三温糖(红糖、蔗糖亦可)10克" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">低筋面粉</div>

<div class="ingredient-unit">20克</div>
<meta content="低筋面粉20克" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">香草糖(白砂糖、上白糖亦可)</div>

<div class="ingredient-unit">20克</div>
<meta content="香草糖(白砂糖、上白糖亦可)20克" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">蛋</div>

<div class="ingredient-unit">1颗</div>
<meta content="蛋1颗" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">牛奶</div>

<div class="ingredient-unit">90克</div>
<meta content="牛奶90克" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">糖粉(装饰用，可省略)</div>

<div class="ingredient-unit">适量</div>
<meta content="糖粉(装饰用，可省略)适量" itemprop="recipeIngredient"/></div>

<div class="ingredient" itemprop="ingredients">
<div class="ingredient-name">薄荷叶(装饰用，可省略)</div>

<div class="ingredient-unit">两片</div>
<meta content="薄荷叶(装饰用，可省略)两片" itemprop="recipeIngredient"/></div>
</div>
</div>
</div>
</div>

<div class="recipe-details-steps-note recipe-details-block">
<div class="recipe-details-steps recipe-details-sub-block">
<ul class="steps" itemprop="recipeInstructions">
	<li class="step">
	<div class="step-cover" data-id="1215738">
	<div class="ratio-container ratio-container-4-3"><a class="strip" data-strip-caption="先预热烤箱180度。

将苹果削皮切块，把苹果块、10克奶油、10克三温糖(亦可用红糖或蔗糖如二砂取代)放入小锅，以中火让苹果焦糖化即可取出。(约6分钟，不需把苹果煮软，只要表面呈焦糖褐色即可。)
" data-strip-group="recipe-imgs" href="https://tokyo-kitchen.icook.network/uploads/step/cover/1215738/large_9bb1bc6651cb3b38.jpg"><img alt="先预热烤箱180度。

将苹果削皮切块，把苹果块、10克奶油、10克三温糖(亦可用红糖或蔗糖如二砂取代)放入小锅，以中火让苹果焦糖化即可取出。(约6分钟，不需把苹果煮软，只要表面呈焦糖褐色即可。)
" class="lazyload" height="600px" onerror="window.__iCook_srcsetFallback &amp;&amp; __iCook_srcsetFallback(this);" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772827_4.jpg" srcset="https://imageproxy.icook.network/resize?nocrop=true&amp;sign=77v6Bala1K5wo5nu9xV9LkzlbSTSEmggTcE22uSdhrg&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215738%2Fmedium_9bb1bc6651cb3b38.jpg&amp;width=220 220w, https://imageproxy.icook.network/resize?nocrop=true&amp;sign=qELtL1PgdvO1S6YJPtGYGhTabCFyxRkWODFnSyoa0Yo&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215738%2Fmedium_9bb1bc6651cb3b38.jpg&amp;width=400 400w" width="800px" /> </a></div>
	</div>

	<div class="step-instruction"><big>1</big>

	<div class="step-instruction-content"><!--
-->先预热烤箱180度。 将苹果削皮切块，把苹果块、10克奶油、10克三温糖(亦可用红糖或蔗糖如二砂取代)放入小锅，以中火让苹果焦糖化即可取出。(约6分钟，不需把苹果煮软，只要表面呈焦糖褐色即可。) <!--
--></div>
	</div>
	</li>
	<li class="step">
	<div class="step-cover" data-id="1215735">
	<div class="ratio-container ratio-container-4-3"><a class="strip" data-strip-caption="料理盆内加入过筛的低筋面粉、香草糖与1颗蛋，搅拌均匀。
再加入牛奶拌至看不见面粉即成蛋奶糊。

(没有香草糖可用白砂糖或上白糖取代。)" data-strip-group="recipe-imgs" href="https://tokyo-kitchen.icook.network/uploads/step/cover/1215735/large_cfa638f430cb9a8e.jpg"><img alt="料理盆内加入过筛的低筋面粉、香草糖与1颗蛋，搅拌均匀。
再加入牛奶拌至看不见面粉即成蛋奶糊。

(没有香草糖可用白砂糖或上白糖取代。)" class="lazyload" height="600px" onerror="window.__iCook_srcsetFallback &amp;&amp; __iCook_srcsetFallback(this);" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772829_5.jpg" srcset="https://imageproxy.icook.network/resize?nocrop=true&amp;sign=Vd1gDR0L7sWL5rOKIiIdG8HKqlKS0JDUHpXWVd_GoJo&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215735%2Fmedium_cfa638f430cb9a8e.jpg&amp;width=220 220w, https://imageproxy.icook.network/resize?nocrop=true&amp;sign=E2n9OmqNPcUM-yRShmrQ6BEsTi3uYcQWEBqi45TAhak&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215735%2Fmedium_cfa638f430cb9a8e.jpg&amp;width=400 400w" width="800px" /> </a></div>
	</div>

	<div class="step-instruction"><big>2</big>

	<div class="step-instruction-content"><!--
-->料理盆内加入过筛的低筋面粉、香草糖与1颗蛋，搅拌均匀。 再加入牛奶拌至看不见面粉即成蛋奶糊。 (没有香草糖可用白砂糖或上白糖取代。)<!--
--></div>
	</div>
	</li>
	<li class="step">
	<div class="step-cover" data-id="1215734">
	<div class="ratio-container ratio-container-4-3"><a class="strip" data-strip-caption="烤盘(约18cm*14cm*4cm)内抹一点奶油(份量外)，将焦糖化的苹果均匀放入烤盘，再倒入拌好的蛋奶糊。" data-strip-group="recipe-imgs" href="https://tokyo-kitchen.icook.network/uploads/step/cover/1215734/large_6f5111fc805b5416.jpg"><img alt="烤盘(约18cm*14cm*4cm)内抹一点奶油(份量外)，将焦糖化的苹果均匀放入烤盘，再倒入拌好的蛋奶糊。" class="lazyload" height="600px" onerror="window.__iCook_srcsetFallback &amp;&amp; __iCook_srcsetFallback(this);" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772830_6.jpg" srcset="https://imageproxy.icook.network/resize?nocrop=true&amp;sign=UTGIUlkggW9kgJ6o8Gj8ik2vwtijqQd4LyFdgu2RZGk&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215734%2Fmedium_6f5111fc805b5416.jpg&amp;width=220 220w, https://imageproxy.icook.network/resize?nocrop=true&amp;sign=29-NJrCfgxiPL1W6Kr2yVNwoMbvOkBEv_e4Cmngqkqg&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215734%2Fmedium_6f5111fc805b5416.jpg&amp;width=400 400w" width="800px" /> </a></div>
	</div>

	<div class="step-instruction"><big>3</big>

	<div class="step-instruction-content"><!--
-->烤盘(约18cm*14cm*4cm)内抹一点奶油(份量外)，将焦糖化的苹果均匀放入烤盘，再倒入拌好的蛋奶糊。<!--
--></div>
	</div>
	</li>
	<li class="step">
	<div class="step-cover" data-id="1215736">
	<div class="ratio-container ratio-container-4-3"><a class="strip" data-strip-caption="将烤盘放入已预热的烤箱，180度烤35分钟左右即可取出。" data-strip-group="recipe-imgs" href="https://tokyo-kitchen.icook.network/uploads/step/cover/1215736/large_014798aba8be3b40.jpg"><img alt="将烤盘放入已预热的烤箱，180度烤35分钟左右即可取出。" class="lazyload" height="600px" onerror="window.__iCook_srcsetFallback &amp;&amp; __iCook_srcsetFallback(this);" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772832_7.jpg" srcset="https://imageproxy.icook.network/resize?nocrop=true&amp;sign=1crq-Aoo1KAv8cKL-3PNE4G1p6sJoXMfqqRZMe0SPSM&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215736%2Fmedium_014798aba8be3b40.jpg&amp;width=220 220w, https://imageproxy.icook.network/resize?nocrop=true&amp;sign=mY1ZxtBFG9tfNmz17F1QUqG_WewvpQiqd4efddfh-tY&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215736%2Fmedium_014798aba8be3b40.jpg&amp;width=400 400w" width="800px" /> </a></div>
	</div>

	<div class="step-instruction"><big>4</big>

	<div class="step-instruction-content"><!--
-->将烤盘放入已预热的烤箱，180度烤35分钟左右即可取出。<!--
--></div>
	</div>
	</li>
	<li class="step">
	<div class="step-cover" data-id="1215737">
	<div class="ratio-container ratio-container-4-3"><a class="strip" data-strip-caption="洒上糖粉，再以薄荷叶装饰，即可享用~
(若没有糖粉和薄荷叶也没关系，还是很好吃唷~)" data-strip-group="recipe-imgs" href="https://tokyo-kitchen.icook.network/uploads/step/cover/1215737/large_9701f011e25933bc.jpg"><img alt="洒上糖粉，再以薄荷叶装饰，即可享用~
(若没有糖粉和薄荷叶也没关系，还是很好吃唷~)" class="lazyload" height="600px" onerror="window.__iCook_srcsetFallback &amp;&amp; __iCook_srcsetFallback(this);" src="http://pih1wob2b.bkt.clouddn.com/icook_1542772833_8.jpg" srcset="https://imageproxy.icook.network/resize?nocrop=true&amp;sign=EQjn9iNI2-9UcLUYi8hDsbxxis8tOjIA00rkV-cIEjQ&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215737%2Fmedium_9701f011e25933bc.jpg&amp;width=220 220w, https://imageproxy.icook.network/resize?nocrop=true&amp;sign=VRs96X5XeAT8edfGs3W8i96vv2L3rqpf1d7f5eCmVpI&amp;stripmeta=true&amp;type=auto&amp;url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Fstep%2Fcover%2F1215737%2Fmedium_9701f011e25933bc.jpg&amp;width=400 400w" width="800px" /> </a></div>
	</div>

	<div class="step-instruction"><big>5</big>

	<div class="step-instruction-content"><!--
-->洒上糖粉，再以薄荷叶装饰，即可享用~ (若没有糖粉和薄荷叶也没关系，还是很好吃唷~)<!--
--></div>
	</div>
	</li>
</ul>
</div>
</div>
</div>
</div>

'''

print(len(tmp))
soup = BeautifulSoup(tmp, "lxml")
recipe_cover = soup.find("div", "recipe-cover")
recipe_cover_img = recipe_cover.find("img")
content = str(recipe_cover_img)
header_row_description = soup.find("div", "header-row description")
header_row_description_p = header_row_description.find("p")
del_header_row_description_a = header_row_description_p.find("a")
header_row_description_p = str(header_row_description_p).replace(str(del_header_row_description_a), "")
content = content +"<br>" + header_row_description_p

servings_info = soup.find("div", "servings-info info-block")
info_tag = servings_info.find("div", "info-tag").text
content = content + info_tag

info_content = servings_info.find("div", "info-content").text
content = content +"<br>" + info_content

time_info = soup.find("div", "time-info info-block")
info_tag = time_info.find("div", "info-tag").text
content = content +"<br>"+info_tag

info_content = time_info.find("div", "info-content").text
content = content +"<br>" + info_content

title_info = soup.find("div", "title").text
content = content +"<br>" + title_info
ingredients = soup.find_all("div", "ingredient")
for x in ingredients:
    ingredient_name = x.find("div", "ingredient-name").text
    content = content + "<br>" + ingredient_name
    ingredient_unit = x.find("div", "ingredient-unit").text
    content = content + "<br>" + ingredient_unit

li_info = soup.find_all("li")
tmp_img = '<img alt="" height="600" src="icook_img" width="800" />'
for y in li_info:
    img = y.find("img").get("src")
    new_img = tmp_img.replace("icook_img", img)
    content = content + "<br>" + new_img
    step_instruction = y.find("big").text
    content = content + "<br>" + step_instruction

    step_instruction_content = y.find("div", "step-instruction-content").text
    content = content + "<br>" + step_instruction_content
print(content)
print(len(content))
