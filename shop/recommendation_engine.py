from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from .models import (
    Product, Category, Zone, ProductView, UserPreference,
    ProductRecommendation, Order, OrderItem, User
)
import random
import math


class ProductRecommendationEngine:
    """
    Advanced product recommendation engine that personalizes product suggestions
    based on user behavior, location, preferences, and various algorithms.
    """

    def __init__(self, user=None, session_id=None, location=None):
        self.user = user
        self.session_id = session_id
        self.location = location  # {'lat': float, 'lng': float}
        self.recommendations = []

    def get_recommendations(self, limit=12, exclude_products=None):
        """
        Get personalized product recommendations for a user.

        Args:
            limit: Number of products to recommend
            exclude_products: List of product IDs to exclude

        Returns:
            List of Product objects with recommendation scores
        """
        if exclude_products is None:
            exclude_products = []

        # Get base products
        base_products = Product.objects.filter(is_available=True).exclude(id__in=exclude_products)

        # Apply different recommendation algorithms
        algorithms = [
            self._location_based_recommendations,
            self._category_based_recommendations,
            self._purchase_history_recommendations,
            self._popular_products,
            self._trending_products,
            self._similar_users_recommendations,
            self._time_based_recommendations,
            self._new_arrivals,
        ]

        all_recommendations = []

        for algorithm in algorithms:
            try:
                recommendations = algorithm(base_products, limit // len(algorithms) + 1)
                all_recommendations.extend(recommendations)
            except Exception as e:
                print(f"Error in {algorithm.__name__}: {e}")
                continue

        # Remove duplicates and sort by score
        seen_products = set()
        unique_recommendations = []

        for rec in all_recommendations:
            if rec['product'].id not in seen_products:
                unique_recommendations.append(rec)
                seen_products.add(rec['product'].id)

        # Sort by score and return top recommendations
        unique_recommendations.sort(key=lambda x: x['score'], reverse=True)
        return unique_recommendations[:limit]

    def _location_based_recommendations(self, base_products, limit):
        """Recommend products from nearby zones"""
        recommendations = []

        if not self.location:
            return recommendations

        # Find nearby zones (simplified - in real app would use proper distance calculation)
        nearby_zones = Zone.objects.filter(is_active=True)

        if self.user and hasattr(self.user, 'profile') and self.user.profile.zone_assigned:
            # Prioritize user's assigned zone
            nearby_zones = nearby_zones.filter(id=self.user.profile.zone_assigned.id)

        zone_products = base_products.filter(zone__in=nearby_zones)[:limit]

        for product in zone_products:
            recommendations.append({
                'product': product,
                'score': 0.9,  # High score for location-based
                'reason': 'location_based'
            })

        return recommendations

    def _category_based_recommendations(self, base_products, limit):
        """Recommend products from user's preferred categories"""
        recommendations = []

        if not self.user:
            return recommendations

        # Get user's preferred categories from views and purchases
        preferred_categories = self._get_user_preferred_categories()

        if preferred_categories:
            category_products = base_products.filter(category__in=preferred_categories)[:limit]

            for product in category_products:
                score = 0.8 if product.category in preferred_categories else 0.6
                recommendations.append({
                    'product': product,
                    'score': score,
                    'reason': 'category_based'
                })

        return recommendations

    def _purchase_history_recommendations(self, base_products, limit):
        """Recommend products similar to user's purchase history"""
        recommendations = []

        if not self.user:
            return recommendations

        # Get user's purchased products
        purchased_products = OrderItem.objects.filter(
            order__customer=self.user,
            order__status__in=['delivered', 'confirmed']
        ).values_list('product', flat=True).distinct()

        if purchased_products:
            # Get categories of purchased products
            purchased_categories = Product.objects.filter(
                id__in=purchased_products
            ).values_list('category', flat=True).distinct()

            # Recommend from same categories
            similar_products = base_products.filter(
                category__in=purchased_categories
            ).exclude(id__in=purchased_products)[:limit]

            for product in similar_products:
                recommendations.append({
                    'product': product,
                    'score': 0.85,
                    'reason': 'purchase_history'
                })

        return recommendations

    def _popular_products(self, base_products, limit):
        """Recommend most popular products (by views and purchases)"""
        recommendations = []

        # Get products with most views in last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)

        popular_products = Product.objects.filter(
            is_available=True,
            productview__viewed_at__gte=thirty_days_ago
        ).annotate(
            view_count=Count('productview')
        ).order_by('-view_count')[:limit]

        for product in popular_products:
            recommendations.append({
                'product': product,
                'score': 0.7,
                'reason': 'popular'
            })

        return recommendations

    def _trending_products(self, base_products, limit):
        """Recommend trending products (recent purchases)"""
        recommendations = []

        seven_days_ago = timezone.now() - timedelta(days=7)

        trending_products = Product.objects.filter(
            is_available=True,
            orderitem__order__created_at__gte=seven_days_ago,
            orderitem__order__status__in=['delivered', 'confirmed']
        ).annotate(
            recent_orders=Count('orderitem')
        ).order_by('-recent_orders')[:limit]

        for product in trending_products:
            recommendations.append({
                'product': product,
                'score': 0.75,
                'reason': 'trending'
            })

        return recommendations

    def _similar_users_recommendations(self, base_products, limit):
        """Recommend products that similar users liked"""
        recommendations = []

        if not self.user:
            return recommendations

        # Find users who bought similar products
        user_purchases = OrderItem.objects.filter(
            order__customer=self.user
        ).values_list('product__category', flat=True).distinct()

        if user_purchases:
            # Find other users who bought from same categories
            similar_users = User.objects.filter(
                order__items__product__category__in=user_purchases
            ).exclude(id=self.user.id).distinct()[:10]

            if similar_users:
                # Get products bought by similar users
                similar_user_products = Product.objects.filter(
                    orderitem__order__customer__in=similar_users,
                    is_available=True
                ).exclude(
                    orderitem__order__customer=self.user
                ).distinct()[:limit]

                for product in similar_user_products:
                    recommendations.append({
                        'product': product,
                        'score': 0.65,
                        'reason': 'similar_users'
                    })

        return recommendations

    def _time_based_recommendations(self, base_products, limit):
        """Recommend products based on time of day"""
        recommendations = []
        current_hour = timezone.now().hour

        # Morning: Breakfast items
        if 6 <= current_hour < 12:
            time_products = base_products.filter(
                Q(title__icontains='নাস্তা') |
                Q(title__icontains='পরোটা') |
                Q(title__icontains='দুধ') |
                Q(category__name__icontains='নাস্তা')
            )[:limit//2]

        # Afternoon/Evening: General items
        elif 12 <= current_hour < 18:
            time_products = base_products.filter(
                Q(title__icontains='খাবার') |
                Q(title__icontains='মাছ') |
                Q(title__icontains='মাংস')
            )[:limit//2]

        # Night: Snacks and light items
        else:
            time_products = base_products.filter(
                Q(title__icontains='চা') |
                Q(title__icontains='বিস্কুট') |
                Q(title__icontains='ফল')
            )[:limit//2]

        for product in time_products:
            recommendations.append({
                'product': product,
                'score': 0.6,
                'reason': 'time_based'
            })

        return recommendations

    def _new_arrivals(self, base_products, limit):
        """Recommend newly added products"""
        recommendations = []

        seven_days_ago = timezone.now() - timedelta(days=7)
        new_products = base_products.filter(created_at__gte=seven_days_ago)[:limit//2]

        for product in new_products:
            recommendations.append({
                'product': product,
                'score': 0.55,
                'reason': 'new_arrivals'
            })

        return recommendations

    def _get_user_preferred_categories(self):
        """Get user's preferred categories based on behavior"""
        if not self.user:
            return []

        preferred_categories = []

        # From purchase history
        purchased_categories = Category.objects.filter(
            products__orderitem__order__customer=self.user
        ).distinct()

        # From viewed products
        viewed_categories = Category.objects.filter(
            products__productview__user=self.user
        ).distinct()

        # Combine and return
        preferred_categories = list(purchased_categories) + list(viewed_categories)
        return list(set(preferred_categories))  # Remove duplicates

    def track_product_view(self, product):
        """Track when a user views a product"""
        if self.user:
            ProductView.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'session_id': self.session_id or ''}
            )
        elif self.session_id:
            ProductView.objects.get_or_create(
                user=None,
                product=product,
                session_id=self.session_id
            )

    def update_user_preferences(self, category=None, zone=None, product=None):
        """Update user preferences based on interactions"""
        if not self.user:
            return

        preference, created = UserPreference.objects.get_or_create(user=self.user)

        if category:
            preference.preferred_categories.add(category)

        if zone:
            preference.preferred_zones.add(zone)

        if product:
            preference.favorite_products.add(product)

        if self.location:
            preference.last_location_lat = self.location.get('lat')
            preference.last_location_lng = self.location.get('lng')

        preference.save()


def get_personalized_products(user=None, session_id=None, location=None, limit=12, exclude_products=None):
    """
    Main function to get personalized product recommendations.

    Args:
        user: User object (if authenticated)
        session_id: Session ID for anonymous users
        location: Dict with 'lat' and 'lng' keys
        limit: Number of products to return
        exclude_products: List of product IDs to exclude

    Returns:
        List of Product objects
    """
    engine = ProductRecommendationEngine(user=user, session_id=session_id, location=location)
    recommendations = engine.get_recommendations(limit=limit, exclude_products=exclude_products)

    # Return just the products (not the full recommendation objects)
    return [rec['product'] for rec in recommendations]