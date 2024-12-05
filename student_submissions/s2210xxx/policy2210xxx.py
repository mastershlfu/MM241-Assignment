from policy import Policy
import numpy as np
import pulp as lp
import random

class Policy2210xxx(Policy):
   
# SA (Simulated Annealing)
    def __init__(self, initial_temp=100, cooling_rate=0.99):
        """
        Khởi tạo policy sử dụng Simulated Annealing (SA).
        :param initial_temp: Nhiệt độ ban đầu cho thuật toán SA.
        :param cooling_rate: Tỷ lệ giảm nhiệt độ.
        """
        self.temp = initial_temp
        self.cooling_rate = cooling_rate

    def get_action(self, observation, info):
        """
        Lấy hành động bằng cách áp dụng Simulated Annealing để tìm giải pháp tốt nhất.
        :param observation: Trạng thái hiện tại của môi trường.
        :param info: Thông tin bổ sung từ môi trường.
        :return: Từ điển chứa stock_idx, size, và position.
        """
        products = observation["products"]
        stocks = observation["stocks"]

        # Sinh giải pháp ban đầu
        current_solution = self._generate_initial_solution(products, stocks)
        best_solution = current_solution

        # Bắt đầu vòng lặp Simulated Annealing
        while self.temp > 1:
            # Sinh giải pháp lân cận
            neighbor_solution = self._generate_neighbor_solution(current_solution, products, stocks)

            # Đánh giá năng lượng của các giải pháp
            current_energy = self._evaluate_solution(current_solution, products, stocks)
            neighbor_energy = self._evaluate_solution(neighbor_solution, products, stocks)

            # Quyết định chấp nhận giải pháp lân cận
            if self._acceptance_probability(current_energy, neighbor_energy, self.temp) > random.random():
                current_solution = neighbor_solution

            # Cập nhật giải pháp tốt nhất
            if neighbor_energy < self._evaluate_solution(best_solution, products, stocks):
                best_solution = neighbor_solution

            # Giảm nhiệt độ
            self.temp *= self.cooling_rate

        # Trả về giải pháp tốt nhất
        return best_solution

    def _generate_initial_solution(self, products, stocks):
        """
        Sinh giải pháp ban đầu ngẫu nhiên.
        """
        for i, product in enumerate(products):
            if product["quantity"] > 0:
                for j, stock in enumerate(stocks):
                    stock_w, stock_h = self._get_stock_size_(stock)
                    prod_w, prod_h = product["size"]

                    for x_pos in range(stock_w - prod_w + 1):
                        for y_pos in range(stock_h - prod_h + 1):
                            if self._can_place_(stock, (x_pos, y_pos), (prod_w, prod_h)):
                                return {"stock_idx": j, "size": (prod_w, prod_h), "position": (x_pos, y_pos)}
        return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}

    def _generate_neighbor_solution(self, current_solution, products, stocks):
        """
        Sinh giải pháp lân cận bằng cách thay đổi vị trí ngẫu nhiên.
        """
        stock_idx = current_solution["stock_idx"]
        if stock_idx == -1:
            return current_solution

        stock = stocks[stock_idx]
        stock_w, stock_h = self._get_stock_size_(stock)

        prod_w, prod_h = current_solution["size"]
        x_pos = random.randint(0, stock_w - prod_w)
        y_pos = random.randint(0, stock_h - prod_h)

        if self._can_place_(stock, (x_pos, y_pos), (prod_w, prod_h)):
            return {"stock_idx": stock_idx, "size": (prod_w, prod_h), "position": (x_pos, y_pos)}
        return current_solution

    def _evaluate_solution(self, solution, products, stocks):
        """
        Đánh giá năng lượng của giải pháp: Diện tích lãng phí.
        """
        stock_idx = solution["stock_idx"]
        if stock_idx == -1:
            return float("inf")  # Không đặt được sản phẩm => năng lượng cực cao

        stock = stocks[stock_idx]
        stock_w, stock_h = self._get_stock_size_(stock)
        prod_w, prod_h = solution["size"]

        # Tính lãng phí: Phần còn lại của kho sau khi đặt sản phẩm
        wasted_area = (stock_w * stock_h) - (prod_w * prod_h)
        return wasted_area

    def _acceptance_probability(self, current_energy, neighbor_energy, temp):
        """
        Tính xác suất chấp nhận giải pháp kém hơn dựa trên nhiệt độ.
        """
        if neighbor_energy < current_energy:
            return 1.0
        return np.exp((current_energy - neighbor_energy) / temp)
#--------------------------------------------------------------------------------------------------------------------------------------
# new dp
    # def get_action(self, observation, info):
    #     list_prods = observation["products"]

    #     prod_size = [0, 0]
    #     stock_idx = -1
    #     pos_x, pos_y = 0, 0

    #     for prod in list_prods:
    #         if prod["quantity"] > 0:
    #             prod_size = prod["size"]

    #             # Iterate through all stocks to find the best placement
    #             for i, stock in enumerate(observation["stocks"]):
    #                 position = self._find_best_position_dp(stock, prod_size)
    #                 if position:
    #                     pos_x, pos_y = position
    #                     stock_idx = i
    #                     break

    #             if stock_idx != -1:
    #                 break

    #     return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
    
    # def _find_best_position_dp(self, stock, prod_size):
    #     stock_w, stock_h = stock.shape
    #     prod_w, prod_h = prod_size

    #     # Xác minh nếu sản phẩm lớn hơn không gian kho
    #     if prod_w > stock_w or prod_h > stock_h:
    #         return None

    #     # Sử dụng ma trận boolean để đánh dấu vùng trống
    #     available_space = (stock == -1)
    #     best_position = None
    #     min_unused_space = float('inf')

    #     for i in range(stock_w - prod_w + 1):
    #         for j in range(stock_h - prod_h + 1):
    #             # Kiểm tra vùng hiện tại có khả dụng không
    #             sub_region = available_space[i:i + prod_w, j:j + prod_h]
    #             if sub_region.shape != (prod_w, prod_h):
    #                 continue
    #             if np.all(sub_region):  # Vùng trống đủ lớn
    #                 unused_space = (stock_w * stock_h) - (prod_w * prod_h)
    #                 if unused_space < min_unused_space:
    #                     min_unused_space = unused_space
    #                     best_position = (i, j)

    #     return best_position