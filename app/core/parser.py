import logging
from datetime import datetime, timezone

import httpx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_product_data(artikul: str):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"

    logger.info(f"Fetching product data for artikul: {artikul} from URL: {url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            logger.info(f"Response status: {response.status_code}")
            data = response.json()

            product_data = data.get("data", {}).get("products", [{}])[0]
            if not product_data:
                logger.warning(f"No product found for artikul: {artikul}")
                return None

            total_stock = sum(
                stock["qty"] for size in product_data.get("sizes", []) for stock in size.get("stocks", [])
            )

            naive_created_at = datetime.now(timezone.utc).replace(tzinfo=None)

            return {
                "artikul": artikul,
                "name": product_data.get("name"),
                "price": product_data.get("salePriceU", 0) / 100,
                "rating": product_data.get("rating"),
                "stock": total_stock,
                "created_at": naive_created_at,
            }

        except httpx.RequestError as e:
            logger.error(f"An error occurred while fetching product data: {e}")
            return None
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
