// for add to cart action

hovermodals = document.getElementsByClassName('product-action-2')
console.log(hovermodals)
for(i=0;i<hovermodals.length;i++){
	hovermodals[i].addEventListener('click',function() {
		console.log(this.dataset.product_id,this.dataset.price)
		document.getElementsByClassName('total-count')[0].innerHTML ++

	})
}