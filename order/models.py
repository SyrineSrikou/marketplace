from django.db import models
from accounts.models import Address, User
from store.models import Product, Store


class Order(models.Model):

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    stores = models.ManyToManyField(Store, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address =models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']
    
  

    ''' def update_inventory(self, num_available, save=False):
        if not self.inventory_updated and self.product:
            self.product.remove_items_from_inventory(quantity, save=True)
            self.inventory_updated = True
        if save == True:
            self.save()
        return self.save '''

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    store_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' % self.id
    
    def __str__(self):
        return self.product.name

    def get_total_price(self):
        return self.price * self.quantity

    """  def update_inventory(self, stock, save=False):
        if not self.inventory_updated and self.product:
            self.product.remove_items_from_inventory(quantity, save=True)
            self.inventory_updated = True
        if save == True:
            self.save()
        return self.save """

    